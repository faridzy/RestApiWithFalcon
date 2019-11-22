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
from app.model import Products
from app.errors import AppError, InvalidParameterError,DataNotFound

LOG = log.get_logger()

FIELDS = {
    'product_name': {
        'type': 'string',
        'required': True,
        'minlength': 4,
        'maxlength': 255
    },
    'description': {
        'type': 'string',
        'required': True,
        'minlength': 4,
        'maxlength': 255
    },
    'price': {
        'type': 'float',
        'required': True,
        'minlength': 4,
        'maxlength': 255
    },
    'vendor_id': {
        'type': 'integer',
        'required': False,
    },
    'product_type_id': {
        'type': 'integer',
        'required': False,
    },
    'id': {
        'type': 'integer',
        'required': False,
    }

}


def validation(req, res, resource, params):
    schema = {
        'product_type_id':FIELDS['product_type_id'],
        'vendor_id':FIELDS['vendor_id'],
        'price':FIELDS['price'],
        'description':FIELDS['description'],
        'product_name': FIELDS['product_name'],
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
            data = Products()
            data.product_name = request['product_name']
            data.description=request['description']
            data.price=request['price']
            data.vendor_id=request['vendor_id']
            data.product_type_id=request['product_type_id']
            session.add(data)
            self.on_success(res, None)
        else:
            raise InvalidParameterError(req.context['data'])

    @falcon.before(auth_required)
    def on_get(self, req, res):
        session = req.context['session']
        allData =Products.find_all(session)
        if allData:
            obj = []
            i=1
            for data in allData:
                temp_obj = {
                    'rownum':i,
                    "id": data[0],
                    "product_name":data[1],
                    "description":data[2],
                    "price":data[3],
                    "vendor_name":data[4],
                    'product_type_name':data[5]
                }
                i+=1
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
                Products.find_update(session, request['id'], request)
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
            data = Products.find_one(session, id)
            self.on_success(res, data.to_dict())
        except NoResultFound:
            raise DataNotFound()

    @falcon.before(auth_required)
    def on_delete(self, req, res, id):
        session = req.context['session']
        try:
            Products.find_delete(session, id)
            self.on_success(res, None)
        except NoResultFound:
            raise DataNotFound()


