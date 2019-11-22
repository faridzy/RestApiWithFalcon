# Created by PyCharm.
# User: mfarid

from sqlalchemy import Column
from sqlalchemy import String,BigInteger
from app.model import Base


class Countries(Base):
    id = Column(BigInteger, primary_key=True)
    country_name=Column(String(255),nullable=False)

    def __repr__(self):
        return "<Countries(id='%s',country_name='%s')>" % \
               (self.id,self.country_name)

    @classmethod
    def get_id(cls):
        return Countries.id

    @classmethod
    def find_by_name(cls, session, country_name):
        return session.query(Countries).filter(Countries.country_name == country_name).one()

    FIELDS = {
        'id':int,
        'country_name': str,
    }

    FIELDS.update(Base.FIELDS)
