from api.config.config import db
from enum import Enum

class GenderEnum(str,Enum):
    MALE = "male"
    FEMALE= "female"

class IdEnum(str,Enum):
    NIN= "nin"
    VOTERSCARED= "voters card"
    DRIVERSLICENSE = "driver's license"
    PASSPORT = "passport"

class User(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer(), primary_key= True)
    first_name = db.Column(db.String(), nullable= False)
    last_name = db.Column(db.String(), nullable = False)
    email=db.Column(db.String(), nullable=False, unique=True)
    password= db.Column(db.String(), nullable=False, unique=True)
    gender= db.Column(db.Enum(GenderEnum), nullable=False)
    phone = db.Column(db.String(), nullable=False)
    id_type = db.Column(db.Enum(IdEnum),nullable=False)
    id_number = db.Column(db.String(), nullable = False, unique = True)
    created_at = db.Column(db.DateTime, default = db.func.now())
    updated_at = db.Column(db.DateTime, default = db.func.now(), onupdate= db.func.now())


    def __repr__(self):
        return f"<User {self.email}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()