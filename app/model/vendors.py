# Created by PyCharm.
# User: mfarid

from sqlalchemy import Column
from sqlalchemy import String,BigInteger
from app.model import Base


class Vendors(Base):
    id = Column(BigInteger, primary_key=True)
    vendor_name=Column(String(255),nullable=False)

    def __repr__(self):
        return "<Roles(id='%s'vendor_name='%s')>" % \
               (self.id,self.vendor_name)


    @classmethod
    def get_id(cls):
        return Vendors.id

    @classmethod
    def find_by_name(cls, session, vendor_name):
        return session.query(Vendors).filter(Vendors.vendor_name == vendor_name).one()

    @classmethod
    def find_all(cls, session):
        return session.query(Vendors.id, Vendors.vendor_name).all()

    FIELDS = {
        'id':int,
        'vendor_name': str,
    }

    FIELDS.update(Base.FIELDS)
