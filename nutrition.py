from sqlalchemy import create_engine, Table, Column, DECIMAL, String, MetaData, and_
from sqlalchemy.sql import select
import re
from difflib import SequenceMatcher as SeqMatch

engine = create_engine('mysql://chris:mysql@localhost/USDA_Nutrition')
connector = engine.connect()
metadata = MetaData()

definition = Table('Nutrient_Definition', metadata,
    Column('Nutr_Num', String, primary_key=True),
    Column('Units', String),
    Column('Nutr_Desc', String),
)

food = Table('Food_Description', metadata,
    Column('DBnum', String, primary_key=True),
    Column('FDgroup', String),
    Column('Ldes', String),
    Column('Sdes', String),
    Column('Cname', String),
    Column('RFdes', String),
    Column('Refuse', DECIMAL),
)

foodgroup = Table('Food_Group', metadata,
    Column('Group_Id', String, primary_key=True),
    Column('Description', String),
)

nutrition = Table('Nutrition_Data', metadata,
    Column('DBnum', String, primary_key=True),
    Column('Nutr_Num', String, primary_key=True),
    Column('Nutr_Val', DECIMAL),
    Column('DBnumref', String),
)

weight = Table('Weight', metadata,
    Column('DBnum', String, primary_key=True),
    Column('Seq', String, primary_key=True),
    Column('Amount', DECIMAL),
    Column('Unit', String),
    Column('Grams', DECIMAL),
)

def foodsearch(search):
    """Return 25 most relevant ingredients from database based on search terms.
        
    Keyword arguments:
    search -- string to search for (e.g. 'salted butter')
    """
      
    #split string on certain non text characters
    seaList = re.split('[ ,.;:]', search.lower())
    while(seaList.count('')):
        seaList.remove('')
        
    if not seaList:
        return
    
    s = select([food.c.DBnum, food.c.Ldes])
    
    s = s.where(
            and_(
                *[food.c.Ldes.like('%{}%'.format(word)) for word in seaList]
            )
        )

    result = connector.execute(s).fetchall()
    
    #Sort results based on relevance.
    result = sorted(result,
                    key=lambda row:
                        SeqMatch(
                            None,
                            ''.join(re.split('[ ,]', row[1].lower())),
                            ''.join(seaList),
                        ).ratio(),
                    reverse=True,
                    )
                    
    return [{'code':x[0],'name':x[1]} for x in result[:25]]
    
def nutdata(DBnum):
    """Return the nutrition data for an ingredient.
        
    Keyword arguments:
    dbNum -- database number as a string (e.g. '01001' = Butter, salted)
    """
            
    s = select([nutrition.c.Nutr_Num, nutrition.c.Nutr_Val])
    s = s.where(nutrition.c.DBnum == DBnum)
    
    result = connector.execute(s)
    
    return result
        
def defsearch(nut=None):
    """Return nutrient weight unit and definition.
       
    Keyword arguments:
    nut -- nutrient number as a string (e.g. '203' = protein),
        to show all nutrients exclude this.
    """
    if not isinstance(nut, str):
        nut = str(nut)
        
    result = ''
    s = select([definition.c.Units, definition.c.Nutr_Desc])
    
    if nut:
        s = s.where(definition.c.Nutr_Num == nut)
        
    result = connector.execute(s).fetchall()
    
    for row in result:
        print(row)
        
def wgsearch(DBnum):
    """Return known volumes and weights for an ingredient.
    
    Keyword arguments:
    dbNum -- database number as a string (e.g. '01001' = Butter, salted)
    """    
    s = select(
            [weight.c.Amount, weight.c.Unit, weight.c.Grams],
        ).where(
            weight.c.DBnum == DBnum,
        )
    
    result = connector.execute(s).fetchall()
    
    for row in result:
        print(row)
        
def fgsearch():
    """Return chosen food group number and description that is searchable in database.
    
    Returns:
    returns a tuple ('food group #', 'food group description')
    """
    s = select([foodgroup])
    result = connector.execute(s)
    
    for row in result:
        print(row)

nutdata('01001')
