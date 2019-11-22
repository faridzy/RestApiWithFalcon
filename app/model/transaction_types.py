# Created by PyCharm.
# User: mfarid

from sqlalchemy import Column
from sqlalchemy import String,BigInteger
from app.model import Base


class Transaction_Types(Base):
    id = Column(BigInteger, primary_key=True)
    transaction_type_name=Column(String(255),nullable=False)

    def __repr__(self):
        return "<Transaction_Types(id='%s',transaction_type_name='%s')>" % \
               (self.id,self.transaction_type_name)


    @classmethod
    def get_id(cls):
        return Transaction_Types.id

    @classmethod
    def find_by_name(cls, session, transaction_type_name):
        return session.query(Transaction_Types).filter(Transaction_Types.transaction_type_name == transaction_type_name).one()

    @classmethod
    def find_all(cls, session):
        return session.query(Transaction_Types.id, Transaction_Types.transaction_type_name).all()

    FIELDS = {
        'id':int,
        'transaction_type_name': str,
    }

    FIELDS.update(Base.FIELDS)
