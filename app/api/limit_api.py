from flask_restful import reqparse, abort, Api, Resource


class CheckLimit(Resource):

    def __init__(self, **kwargs):
        self.limit_service = kwargs['limit_service']

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

        return {
            'has_limit': self.limit_service.check_limit(resource_name, access_id)
        }


