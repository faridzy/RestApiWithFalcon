# Created by PyCharm.
# User: mfarid

import falcon
from app.errors import UnauthorizedError


def auth_required(req, res, resource,params):
    if req.context['auth_user'] is None:
        raise UnauthorizedError()
