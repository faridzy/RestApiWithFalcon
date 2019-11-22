# Created by PyCharm.
# User: mfarid

from sqlalchemy import Column
from sqlalchemy import String,BigInteger,Date,ForeignKey
from app.model import Base


class Users(Base):
    id = Column(BigInteger, primary_key=True)
    fullname=Column(String(255),nullable=False)
    username = Column(String(20), nullable=False)
    email = Column(String(320), unique=True, nullable=False)
    password = Column(String(80), nullable=False)
    phone_number=Column(String(20),nullable=True)
    account_number=Column(String(255),nullable=False)
    address=Column(String(255),nullable=True)
    birth_place_city_id=Column(BigInteger,ForeignKey('cities.id'))
    birth_date=Column(Date)
    role_id = Column(BigInteger, ForeignKey('countries.id'))
    token = Column(String(255), nullable=False)

    def __repr__(self):
        return "<User(id='%s',name='%s', email='%s', token='%s',role_id='%s',account_number='%s')>" % \
            (self.id,self.username, self.email, self.token,self.role_id,self.account_number)

    @classmethod
    def get_id(cls):
        return Users.id

    @classmethod
    def find_by_email(cls, session, email):
        return session.query(Users).filter(Users.email == email).one()

    FIELDS = {
        'id':int,
        'username': str,
        'email': str,
        'token': str,
        'role_id':str,
        'account_number':str
    }

    FIELDS.update(Base.FIELDS)
