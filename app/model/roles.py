# Created by PyCharm.
# User: mfarid

from sqlalchemy import Column
from sqlalchemy import String,BigInteger
from app.model import Base


class Roles(Base):
    id = Column(BigInteger, primary_key=True)
    role_name=Column(String(255),nullable=False)

    def __repr__(self):
        return "<Roles(id='%s'role_name='%s')>" % \
               (self.id,self.role_name)


    @classmethod
    def get_id(cls):
        return Roles.id

    @classmethod
    def find_by_name(cls, session, role_name):
        return session.query(Roles).filter(Roles.role_name == role_name).one()

    FIELDS = {
        'id':int,
        'role_name': str,
    }

    FIELDS.update(Base.FIELDS)
