import os, yaml, json
from sqlalchemy.ext.declarative import DeclarativeMeta


class UnableToCompleteAction(Exception):
    status = 400

    def __init__(self, error, status=None):
        Exception.__init__(self)
        self.error = error
        if status is not None:
            self.status = status


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            restrictedFields = [
                "metadata",
                "query",
                "query_class",
                "password",
                "createdAt",
                "updatedAt",
                "isAdmin",
            ]
            for field in [
                x
                for x in dir(obj)
                if not x.startswith("_") and x not in restrictedFields
            ]:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(
                        data
                    )  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


def load_app_config(dir=None):
    APP_CONFIG_YAML = "./config/app.yaml"
    if dir != None:
        APP_CONFIG_YAML = dir
    assert os.path.exists(APP_CONFIG_YAML), "Missing config file: {}".format(
        APP_CONFIG_YAML
    )
    return yaml.safe_load(open(APP_CONFIG_YAML))


def response(data, code):
    return json.dumps(data, cls=AlchemyEncoder), code


def defaultResponse(success=False):

    if success:
        return response({}, 200)
    else:
        return response({"error": "Request Rejected"}, 403)


def notFoundResponse():
    return response(
        {"error": "Unable to Locate Requested Object, ID does not exist"}, 404
    )
