# Created by PyCharm.
# User: mfarid

from sqlalchemy import Column
from sqlalchemy import String,BigInteger
from app.model import Base


class Product_Types(Base):
    id = Column(BigInteger, primary_key=True)
    product_type_name=Column(String(255),nullable=False)

    def __repr__(self):
        return "<Roles(id='%s'product_type_name='%s')>" % \
               (self.id,self.product_type_name)


    @classmethod
    def get_id(cls):
        return Product_Types.id

    @classmethod
    def find_by_name(cls, session, product_type_name):
        return session.query(Product_Types).filter(Product_Types.product_type_name == product_type_name).one()

    @classmethod
    def find_all(cls, session):
        return session.query(Product_Types.id, Product_Types.product_type_name).all()

    FIELDS = {
        'id':int,
        'product_type_name': str,
    }

    FIELDS.update(Base.FIELDS)
