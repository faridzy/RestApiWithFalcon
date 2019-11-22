# Created by PyCharm.
# User: mfarid

import re
import falcon

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import update
from cerberus import Validator, ValidationError

from app import log
from app.api.common import BaseResource
from app.utils.hooks import auth_required
from app.utils.auth import encrypt_token, hash_password, verify_password
from app.model import Users
from app.errors import AppError, InvalidParameterError, UserNotExistsError, PasswordNotMatch, DataNotFound

LOG = log.get_logger()


FIELDS = {
    'fullname': {
        'type': 'string',
        'required': True,
        'minlength': 4,
        'maxlength': 255
    },
    'username': {
        'type': 'string',
        'required': True,
        'minlength': 4,
        'maxlength': 20
    },
    'birth_date': {
        'type': 'string',
        'required': True,
    },
    'phone_number': {
        'type': 'string',
        'required': True,
        'minlength': 11,
        'maxlength': 20
    },
    'account_number': {
        'type': 'integer',
        'required': True,
        'minlength': 16,
        'maxlength': 26
    },
    'email': {
        'type': 'string',
        'regex': '[a-zA-Z0-9._-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,4}',
        'required': True,
        'maxlength': 320
    },
    'password': {
        'type': 'string',
        'regex': '[0-9a-zA-Z]\w{3,14}',
        'required': True,
        'minlength': 8,
        'maxlength': 64
    },
    'role_id': {
        'type': 'integer',
        'required': True,
    },
    'birth_place_city_id': {
        'type': 'integer',
        'required': True,
    },
    'address': {
        'type': 'string',
        'required': True,
        'minlength': 4,
        'maxlength': 20
    },
    'id':{
        'type': 'integer',
        'required': False,
    }

}


def validation(req, res, resource, params):
    schema = {
        'username': FIELDS['username'],
        'email': FIELDS['email'],
        'password': FIELDS['password'],
        'fullname':FIELDS['fullname'],
        'phone_number':FIELDS['phone_number'],
        'account_number':FIELDS['account_number'],
        'role_id':FIELDS['role_id'],
        'birth_place_city_id':FIELDS['birth_place_city_id'],
        'birth_date':FIELDS['birth_date'],
        'address':FIELDS['address'],
        'id':FIELDS['id']
    }

    v = Validator(schema)
    try:
        if not v.validate(req.context['data']):
            raise InvalidParameterError(v.errors)
    except ValidationError:
        raise InvalidParameterError('Invalid Request %s' % req.context)



class Collection(BaseResource):
    """
    /v1/users
    """
    @falcon.before(validation)
    def on_post(self, req, res):
        session = req.context['session']
        request = req.context['data']
        if request:
            data = Users()
            data.fullname=request['fullname']
            data.username = request['username']
            data.email = request['email']
            data.password = hash_password(request['password']).decode('utf-8')
            data.token = encrypt_token(request['password']).decode('utf-8')
            data.phone_number=request['phone_number']
            data.address=request['address']
            data.account_number=request['account_number']
            data.birth_date=request['birth_date']
            data.role_id=request['role_id']
            data.birth_place_city_id=request['birth_place_city_id']
            session.add(data)
            self.on_success(res, None)
        else:
            raise InvalidParameterError(req.context['data'])

    @falcon.before(auth_required)
    def on_get(self, req, res):
        session = req.context['session']
        allData = session.query(Users).all()
        if allData:
            obj = [data.to_dict() for data in allData]
            self.on_success(res, obj)
        else:
            raise AppError()

    @falcon.before(auth_required)
    def on_put(self, req, res):
        session = req.context['session']
        request = req.context['data']
        if request:
            if request['id'] != None:
                Users.find_update(session,request['id'],request)
                self.on_success(res, None)

        else:
            raise InvalidParameterError(req.context['data'])


class Item(BaseResource):
    """
    /v1/users/{user_id}
    """
    @falcon.before(auth_required)
    def on_get(self, req, res,id):
        session = req.context['session']
        try:
            data = Users.find_one(session, id)
            self.on_success(res, data.to_dict())
        except NoResultFound:
            raise DataNotFound()
    @falcon.before(auth_required)
    def on_delete(self, req, res ,id):
        session = req.context['session']
        try:
            Users.find_delete(session,id)
            self.on_success(res,None)
        except NoResultFound:
            raise DataNotFound()
        
class Self(BaseResource):
    """
    /v1/users/self
    """
    LOGIN = 'login'
    RESETPW = 'resetpw'

    def on_post(self, req, res):
        cmd = re.split('\\W+', req.path)[-1:][0]
        if cmd == Self.LOGIN:
            self.process_login(req, res)
        elif cmd == Self.RESETPW:
            self.process_resetpw(req, res)

    def process_login(self, req, res):
        data = req.context['data']
        email = data['email']
        password = data['password']
        session = req.context['session']
        try:
            data = Users.find_by_email(session, email)
            if verify_password(password, data.password.encode('utf-8')):

                self.on_success(res, data.to_dict())
            else:
                raise PasswordNotMatch()
        except NoResultFound:
            raise UserNotExistsError('User email: %s' % email)

    @falcon.before(auth_required)
    def process_resetpw(self, req, res):
        pass
