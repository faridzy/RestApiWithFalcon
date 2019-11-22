# Created by PyCharm.
# User: mfarid

from sqlalchemy import Column
from sqlalchemy import String,BigInteger,Float,ForeignKey
from app.model import Base
from app.model import Vendors
from app.model import Product_Types


class Products(Base):
    id = Column(BigInteger, primary_key=True)
    product_name=Column(String(255),nullable=False)
    description=Column(String(255),nullable=True)
    price=Column(Float,nullable=True)
    vendor_id=Column(BigInteger, ForeignKey('vendors.id'))
    product_type_id=Column(BigInteger, ForeignKey('product_types.id'))

    @classmethod
    def get_id(cls):
        return Products.id

    @classmethod
    def find_by_name(cls, session, product_name):
        return session.query().filter(Products.product_name == product_name).one()

    @classmethod
    def find_all(cls, session):
        return session.query(Products.id,Products.product_name,Products.description,Products.price,Vendors.vendor_name,Product_Types.product_type_name)\
            .join(Vendors).join(Product_Types).filter(Vendors.id == Products.vendor_id)\
            .filter(Product_Types.id == Products.product_type_id).all()

    FIELDS = {
        'id':int,
        'product_name': str,
        'description':str,
        'price':float,
        'vendor_id':int,
        'product_type_id':int
    }



    FIELDS.update(Base.FIELDS)
