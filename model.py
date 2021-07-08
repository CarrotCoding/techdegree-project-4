from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///inventory.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True)
    product_name = Column('Product', String)
    product_quantity = Column('Quantity', Integer)
    product_price = Column('Price', Integer)
    date_updated = Column('Last Updated', Date)


    def __repr__(self):
        return f'Product Name = {self.product_name}, Product Price = {self.product_price}, Quantity = {self.product_quantity}, Last Updated = {self.date_updated}'


    def __str__(self):
        return f'{self.product_name},${self.product_price/100},{self.product_quantity},{self.date_updated.strftime("%m/%d/%Y")}'
