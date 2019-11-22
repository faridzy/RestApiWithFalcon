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
from app.model import Roles
from app.errors import AppError, InvalidParameterError,DataNotFound

LOG = log.get_logger()

FIELDS = {
    'role_name': {
        'type': 'string',
        'required': True,
        'minlength': 4,
        'maxlength': 255
    },
    'id': {
        'type': 'integer',
        'required': False,
    }

}


def validation(req, res, resource, params):
    schema = {
        'role_name': FIELDS['role_name'],
        'id': FIELDS['id']
    }

    v = Validator(schema)
    try:
        if not v.validate(req.context['data']):
            raise InvalidParameterError(v.errors)
    except ValidationError:
        raise InvalidParameterError('Invalid Request %s' % req.context)


class Collection(BaseResource):
    """
    /v1/roles
    """

    @falcon.before(auth_required)
    @falcon.before(validation)
    def on_post(self, req, res):
        session = req.context['session']
        request = req.context['data']
        if request:
            data = Roles()
            data.role_name = request['role_name']
            session.add(data)
            self.on_success(res, None)
        else:
            raise InvalidParameterError(req.context['data'])

    @falcon.before(auth_required)
    def on_get(self, req, res):
        session = req.context['session']
        allData = session.query(Roles).all()
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
                Roles.find_update(session, request['id'], request)
                self.on_success(res, None)

        else:
            raise InvalidParameterError(req.context['data'])


class Item(BaseResource):
    """
    /v1/roles/{role_id}
    """

    @falcon.before(auth_required)
    def on_get(self, req, res, id):
        session = req.context['session']
        try:
            data = Roles.find_one(session, id)
            self.on_success(res, data.to_dict())
        except NoResultFound:
            raise DataNotFound()

    @falcon.before(auth_required)
    def on_delete(self, req, res, id):
        session = req.context['session']
        try:
            Roles.find_delete(session, id)
            self.on_success(res, None)
        except NoResultFound:
            raise DataNotFound()


