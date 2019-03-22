import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
class Category(Base):
    __tablename__ = 'categories'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
       
       return {
           'id'         : self.id,
           'name'       : self.name,
       }
 
class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    description = Column(String(250))
    price = Column(String(8))
    sub = Column(String(250))
    category_id = Column(Integer,ForeignKey('categories.id'))
    category = relationship(Category) 

    @property
    def serialize(self):
       
       return {
           'id'             : self.id,
           'name'           : self.name,
           'description'    : self.description,
           'sub'            : self.sub,
           'price'          : self.price,
           'category'       : self.category_id,
       }
 

engine = create_engine('sqlite:///catalog.db')
 

Base.metadata.create_all(engine)