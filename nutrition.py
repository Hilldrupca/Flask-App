from sqlalchemy import create_engine, Table, Column, DECIMAL, \
                       String, MetaData, and_
from sqlalchemy.sql import select
import re
from difflib import SequenceMatcher as SeqMatch

# Establish connection with database
url = 'mysql://nutrinfo:nutritioninformation@localhost/USDA_Nutrition'
engine = create_engine(url)
connector = engine.connect()
metadata = MetaData()

# Define form of Nutrient_Definition table
definition = Table('Nutrient_Definition', metadata,
    Column('Nutr_Num', String, primary_key=True),
    Column('Units', String),
    Column('Nutr_Desc', String),
)

# Define form of Food_Description table
food = Table('Food_Description', metadata,
    Column('DBnum', String, primary_key=True),
    Column('FDgroup', String),
    Column('Ldes', String),
    Column('Sdes', String),
    Column('Cname', String),
    Column('RFdes', String),
    Column('Refuse', DECIMAL),
)

# Define form of Food_Group table
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

# List of tracked nutrients. More in database than listed here.
nutr_list = {'208': ('Calories','kcal'), '204': ('Fats','g'), '605': ('Trans fats','g'),
        '606': ('Saturated fats','g'), '645': ('Monounsaturated fats','g'),
        '646': ('Polyunsaturated fats','g'), '851': ('Omega-3','g'), '618': ('Omega-6','g'),
        '601': ('Cholesterol','mg'), '205': ('Carbohydrates','g'), '291': ('Fiber','g'),
        '203': ('Protein','g'), '320': ('Vitamin A','mcg'), '404': ('Thiamin (B1)','mg'),
        '405': ('Riboflavin (B2)','mg'), '406': ('Niacin (B3)','mg'), '410': ('Pantothenic acid (B5)','mg'),
        '415': ('Vitamin B6','mg'), '435': ('Folate (B9)','mcg'), '418': ('Vitamin B12','mcg'),
        '401': ('Vitamin C','mg'), '328': ('Vitamin D','mcg'), '323': ('Vitamin E','mg'),
        '430': ('Vitamin K','mcg'), '421': ('Choline','mg'), '301': ('Calcium','mg'),
        '312': ('Copper','mg'), '313': ('Fluoride','mcg'), '303': ('Iron','mg'),
        '304': ('Magnesium','mg'), '315': ('Manganese','mg'), '305': ('Phosphorus','mg'),
        '306': ('Potassium','mg'), '317': ('Selenium','mcg'), '307': ('Sodium','mg'),
        '309': ('Zinc','mg')}

macros = {'208': ('Calories','kcal'), '204': ('Fats','g'), '605': ('Trans fats','g'),
          '606': ('Saturated fats','g'), '645': ('Monounsaturated fats','g'),
          '646': ('Polyunsaturated fats','g'), '851': ('Omega-3','g'), '618': ('Omega-6','g'),
          '601': ('Cholesterol','mg'),'205': ('Carbohydrates','g'), '291': ('Fiber','g'),
          '203': ('Protein','g')}

vitamins = {'320': ('Vitamin A','mcg'), '404': ('Thiamin (B1)','mg'),
            '405': ('Riboflavin (B2)','mg'), '406': ('Niacin (B3)','mg'),
            '410': ('Pantothenic acid (B5)','mg'), '415': ('Vitamin B6','mg'),
            '435': ('Folate (B9)','mcg'), '418': ('Vitamin B12','mcg'),
            '401': ('Vitamin C','mg'), '328': ('Vitamin D','mcg'), '323': ('Vitamin E','mg'),
            '430': ('Vitamin K','mcg'), '421': ('Choline','mg')}

minerals = {'301': ('Calcium','mg'), '312': ('Copper','mg'), '313': ('Fluoride','mcg'),
            '303': ('Iron','mg'), '304': ('Magnesium','mg'),'315': ('Manganese','mg'),
            '305': ('Phosphorus','mg'), '306': ('Potassium','mg'), '317': ('Selenium','mcg'),
            '307': ('Sodium','mg'), '309': ('Zinc','mg')}

def foodsearch(search):
    '''
    Return 25 most relevant ingredients from database based on search terms.
        
    Params:
        search - String to search for (e.g. 'salted butter')
    '''
      
    #split string on certain non text characters
    seaList = re.split('[ ,.;:]', search.lower())
    while(seaList.count('')):
        seaList.remove('')
        
    if not seaList:
        return
    
    s = select([food.c.DBnum, food.c.Ldes])
    
    s = s.where(
            and_(
                *[food.c.Ldes.like(f'%{word}%') for word in seaList]
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
    '''
    Returns the nutrition data for an ingredient in JSON serializable format.
        
    Params:
        dbNum - Database number as a string (e.g. '01001' = Butter, salted)
    '''
            
    s = select([nutrition.c.Nutr_Num, nutrition.c.Nutr_Val])
    s = s.where(nutrition.c.DBnum == DBnum)
    
    result = connector.execute(s).fetchall()
    json = {}
    for x in result:
        if x[0] in nutr_list:
            name = nutr_list[x[0]]
            # key will be nutrient name, i.e. 'Protein'
            json[name[0]] = str(x[1])

    return json
        
def defsearch(nut=None):
    """
    ### To-Do
    
    Return nutrient weight unit and definition.
       
    Params:
        nut - Nutrient number as a string (e.g. '203' = protein),
              to show all nutrients exclude this.
    """
    if not isinstance(nut, str):
        nut = str(nut)
        
    result = ''
    s = select([definition.c.Units, definition.c.Nutr_Desc])
    
    if nut:
        s = s.where(definition.c.Nutr_Num == nut)
        
    result = connector.execute(s).fetchall()
        
def wgsearch(DBnum):
    '''
    ### To-Do
    
    Return known volumes and weights for an ingredient.
    
    Params:
        dbNum - Database number as a string (e.g. '01001' = Butter, salted)
    '''    
    s = select(
            [weight.c.Amount, weight.c.Unit, weight.c.Grams],
        ).where(
            weight.c.DBnum == DBnum,
        )
    
    result = connector.execute(s).fetchall()
        
def fgsearch():
    '''
    ### To-Do
    
    Return chosen food group number and description that is searchable in
    database.
    
    Returns:
        tuple - ('food group #', 'food group description')
    '''
    s = select([foodgroup])
    result = connector.execute(s)
    


