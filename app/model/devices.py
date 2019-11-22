# Created by PyCharm.
# User: mfarid

from sqlalchemy import Column
from sqlalchemy import String,BigInteger
from app.model import Base


class Devices(Base):
    id = Column(BigInteger, primary_key=True)
    device_name=Column(String(255),nullable=False)
    description=Column(String(255),nullable=True)

    def __repr__(self):
        return "<Device(id='%s',device_name='%s',description='%s')>" % \
               (self.id,self.device_name,self.description)

    @classmethod
    def get_id(cls):
        return Devices.id

    @classmethod
    def find_by_name(cls, session, device_name):
        return session.query(Devices).filter(Devices.device_name == device_name).one()

    @classmethod
    def find_all(cls, session):
        return session.query(Devices.id,Devices.device_name,Devices.description).all()

    FIELDS = {
        'id':int,
        'device_name': str,
        'description':str
    }

    FIELDS.update(Base.FIELDS)
