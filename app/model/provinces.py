# Created by PyCharm.
# User: mfarid

from sqlalchemy import Column
from sqlalchemy import String,BigInteger,Float,ForeignKey
from app.model import Base
from app.model import Countries


class Provinces(Base):
    id = Column(BigInteger, primary_key=True)
    province_name=Column(String(255),nullable=False)
    longitude=Column(Float,nullable=True)
    latitude=Column(Float,nullable=True)
    country_id=Column(BigInteger, ForeignKey('countries.id'))

    @classmethod
    def get_id(cls):
        return Provinces.id

    @classmethod
    def find_by_name(cls, session, province_name):
        return session.query(Provinces).filter(Provinces.province_name == province_name).one()

    @classmethod
    def find_all(cls, session):
        return session.query(Provinces.id,Provinces.province_name,Provinces.latitude,Provinces.longitude,Countries.country_name).join(Countries).filter(Countries.id == Provinces.country_id).all()

    FIELDS = {
        'id':int,
        'province_name': str,
        'country_id':int,
        'longitude':float,
        'latitude':float,
    }



    FIELDS.update(Base.FIELDS)
