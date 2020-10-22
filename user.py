from sqlalchemy import create_engine, Table, Column, Integer, String, Boolean, MetaData, and_
from sqlalchemy.sql import select, insert
from werkzeug.security import generate_password_hash, check_password_hash

engine = create_engine('mysql://userinfo:credentialchecker@localhost/User_Information')
connector = engine.connect()
metadata = MetaData()

credentials = Table('User_Credentials', metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String, unique=True),
    Column('email', String),
    Column('password_hash', String),
    Column('authenticated', Integer)
)

class User:
    
    def __init__(self, id=None, username=None, auth=None):
        self.id = id
        
        if id and username and auth:
            self.username = username
            self.authenticated = auth
        
        elif id:
            s = select([credentials.c.username, credentials.c.authenticated])
            s = s.where(credentials.c.id == self.id)
            self.username, self.authenticated = connector.execute(s).fetchone()
            
        
    @property
    def is_active(self):
        return True
    
    @property
    def is_authenticated(self):        
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self.id
    
    def get_user(self, user_id):
        usr = self.__init__(user_id)
        if usr:
            return usr
        return None
    
    def validate_credentials(self, username=None, password=None):
        if not username or not password:
            return False
        
        s = select([credentials.c.id, credentials.c.username,
                    credentials.c.password_hash, credentials.c.authenticated])
        
        s = s.where(credentials.c.username == username)
        
        id, usr, psw, auth = connector.execute(s).fetchone()

        if check_password_hash(psw, password):
            self.id = id
            self.username = usr
            self.authenticated = 1
            #return User(id, usr, auth)
            
        else:
            return False
        
    def create_account(self, username=None, password=None, email=None):
        return
