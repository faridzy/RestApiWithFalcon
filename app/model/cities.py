# Created by PyCharm.
# User: mfarid

from sqlalchemy import Column
from sqlalchemy import String,BigInteger,Float,ForeignKey
from app.model import Base
from app.model import Provinces


class Cities(Base):
    id = Column(BigInteger, primary_key=True)
    city_name=Column(String(255),nullable=False)
    longitude=Column(Float,nullable=True)
    latitude=Column(Float,nullable=True)
    province_id=Column(BigInteger, ForeignKey('provinces.id'))

    @classmethod
    def get_id(cls):
        return Cities.id

    @classmethod
    def find_by_name(cls, session, city_name):
        return session.query(Cities).filter(Cities.city_name == city_name).one()

    @classmethod
    def find_all(cls, session):
        return session.query(Cities.id,Cities.city_name,Cities.longitude,Cities.latitude,Provinces.province_name)\
            .join(Provinces).filter(Cities.province_id == Provinces.id).all()

    FIELDS = {
        'city_name': str,
        'province_id':int,
        'longitude':float,
        'latitude':float
    }

    FIELDS.update(Base.FIELDS)
