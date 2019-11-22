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
from app.model import Provinces
from app.errors import AppError, InvalidParameterError,DataNotFound

LOG = log.get_logger()

FIELDS = {
    'province_name': {
        'type': 'string',
        'required': True,
        'minlength': 4,
        'maxlength': 255
    },
    'longitude': {
        'type': 'float',
        'required': True,
        'minlength': 4,
        'maxlength': 255
    },
    'latitude': {
        'type': 'float',
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
        'longitude':FIELDS['longitude'],
        'latitude':FIELDS['latitude'],
        'province_name': FIELDS['province_name'],
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
    /v1/provinces
    """

    @falcon.before(auth_required)
    @falcon.before(validation)
    def on_post(self, req, res):
        session = req.context['session']
        request = req.context['data']
        if request:
            data = Provinces()
            data.province_name = request['province_name']
            data.longitude=request['longitude']
            data.latitude=request['latitude']
            session.add(data)
            self.on_success(res, None)
        else:
            raise InvalidParameterError(req.context['data'])

    @falcon.before(auth_required)
    def on_get(self, req, res):
        session = req.context['session']
        allData =Provinces.find_all(session)
        if allData:
            obj = []
            i = 1
            for data in allData:
                temp_obj = {
                    "rownum":i,
                    "id": data[0],
                    "province_name":data[1],
                    "latitude":data[2],
                    "longitude":data[3],
                    "country_name":data[4]
                }
                i += 1
                obj.append(temp_obj)
            self.on_success(res,obj)
        else:
            raise AppError()

    @falcon.before(auth_required)
    def on_put(self, req, res):
        session = req.context['session']
        request = req.context['data']
        if request:
            if request['id'] != None:
                Provinces.find_update(session, request['id'], request)
                self.on_success(res, None)

        else:
            raise InvalidParameterError(req.context['data'])


class Item(BaseResource):
    """
    /v1/provinces/{role_id}
    """

    @falcon.before(auth_required)
    def on_get(self, req, res, id):
        session = req.context['session']
        try:
            data = Provinces.find_one(session, id)
            self.on_success(res, data.to_dict())
        except NoResultFound:
            raise DataNotFound()

    @falcon.before(auth_required)
    def on_delete(self, req, res, id):
        session = req.context['session']
        try:
            Provinces.find_delete(session, id)
            self.on_success(res, None)
        except NoResultFound:
            raise DataNotFound()


