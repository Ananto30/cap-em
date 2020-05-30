from flask_restful import reqparse, Resource

from app.service.limit_service import LimitService


class CheckLimit(Resource):

    def __init__(self, **kwargs):
        self.limit_service: LimitService = kwargs['limit_service']

    @staticmethod
    def parse_args():
        parser = reqparse.RequestParser()
        parser.add_argument('resource_name', type=str, required=True, location='json')
        parser.add_argument('access_id', type=str, required=True, location='json')
        return parser.parse_args()

    def post(self):
        args = self.parse_args()
        resource_name = args['resource_name'].strip()
        access_id = args['access_id'].strip()

        has_limit, access_in = self.limit_service.check_limit(resource_name, access_id)

        return {
            'has_limit': has_limit,
            'access_in': access_in
        }


class AddUsage(Resource):

    def __init__(self, **kwargs):
        self.limit_service: LimitService = kwargs['limit_service']

    @staticmethod
    def parse_args():
        parser = reqparse.RequestParser()
        parser.add_argument('resource_name', type=str, required=True, location='json')
        parser.add_argument('access_id', type=str, required=True, location='json')
        return parser.parse_args()

    def post(self):
        args = self.parse_args()
        resource_name = args['resource_name'].strip()
        access_id = args['access_id'].strip()

        self.limit_service.add_usage(resource_name, access_id)

        return
