# Created by PyCharm.
# User: mfarid

import falcon

from app import log
from app.middleware import AuthHandler, JSONTranslator, DatabaseSessionManager
from app.database import db_session, init_session

from app.api.common import base
from app.api.v1 import users
from app.api.v1 import countries
from app.api.v1 import roles
from app.api.v1 import vendors
from app.api.v1 import product_types
from app.api.v1 import transaction_types
from app.api.v1 import provinces
from app.api.v1 import cities
from app.api.v1 import products
from app.api.v1 import devices
from app.errors import AppError

LOG = log.get_logger()


class App(falcon.API):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        LOG.info('API Server is starting')

        self.add_route('/', base.BaseResource())
        self.add_route('/v1/users', users.Collection())
        self.add_route('/v1/users/{id}', users.Item())
        self.add_route('/v1/countries', countries.Collection())
        self.add_route('/v1/countries/{id}', countries.Item())
        self.add_route('/v1/provinces', provinces.Collection())
        self.add_route('/v1/provinces/{id}', provinces.Item())
        self.add_route('/v1/cities', cities.Collection())
        self.add_route('/v1/cities/{id}', cities.Item())
        self.add_route('/v1/roles', roles.Collection())
        self.add_route('/v1/roles/{id}', roles.Item())
        self.add_route('/v1/vendors', vendors.Collection())
        self.add_route('/v1/vendors/{id}', vendors.Item())
        self.add_route('/v1/devices', devices.Collection())
        self.add_route('/v1/devices/{id}', devices.Item())
        self.add_route('/v1/product_types', product_types.Collection())
        self.add_route('/v1/product_types/{id}', product_types.Item())
        self.add_route('/v1/products', products.Collection())
        self.add_route('/v1/products/{id}', products.Item())
        self.add_route('/v1/transaction_types', transaction_types.Collection())
        self.add_route('/v1/transaction_types/{id}', transaction_types.Item())
        self.add_route('/v1/users/self/login', users.Self())

        self.add_error_handler(AppError, AppError.handle)

init_session()
middleware = [AuthHandler(), JSONTranslator(), DatabaseSessionManager(db_session)]
application = App(middleware=middleware)


if __name__ == "__main__":
    from wsgiref import simple_server
    httpd = simple_server.make_server('127.0.0.1', 5000, application)
    httpd.serve_forever()
