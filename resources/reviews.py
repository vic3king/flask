from flask import jsonify, Blueprint, abort

from flask.ext.restful import Resource, Api, reqparse, inputs, fields, marshal, marshal_with, url_for

import models

review_fields = {
    'id': fields.Integer,
    'for_course': fields.String,
    'rating': fields.Integer,
    'comment': fields.String,
    'created_at': fields.DateTime
}

def review_or_404(review_id):
    try:
        review = models.Review.get(models.Review.id == review_id)
    except models.Review.DoesNotExist:
        abort(404, {"message": f"review {review_id} does not exist"})
    else:
        return review

def add_course(review):
    review.for_course = url_for('resources.courses.course', id=review.course.id)
    return review
    

class ReviewsList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'course',
            required=True,
            help='No course id provided',
            location=['form', 'json'],
            type=inputs.positive
        )
        self.reqparse.add_argument(
            'rating',
            required=True,
            help='No rating provided',
            location=['form', 'json'],
            type=inputs.int_range(1, 5)
        )
        self.reqparse.add_argument(
            'comment',
            required=False,
            nullable=True,
            default='',
            location=['form', 'json'],
        )
        super().__init__()

    def get(self):
         reviews = [marshal(review, review_fields) for review in models.Review.select()]
         return jsonify({'reviews': reviews})

    def post(self):
        args = self.reqparse.parse_args()
        review = models.Review.create(**args)
        return add_course(review)

class Review(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'course',
            required=True,
            help='No course id provided',
            location=['form', 'json'],
            type=inputs.positive
        )
        self.reqparse.add_argument(
            'rating',
            required=True,
            help='No rating provided',
            location=['form', 'json'],
            type=inputs.int_range(1, 5)
        )
        self.reqparse.add_argument(
            'comment',
            required=False,
            nullable=True,
            default='',
            location=['form', 'json'],
        )
        super().__init__()


    @marshal_with(review_fields)
    def get(self, id):
        return review_or_404(id)
    
    def post(self, id):
        args = self.reqparse.parse_args()
        return jsonify({'course': 1, 'rating': 5})

    def put(self, id):
        return jsonify({'course': 1, 'rating': 5})

    def delete(self, id):
        return jsonify({'course': 1, 'rating': 5})


reviews_api = Blueprint('resources.reviews', __name__)
api = Api(reviews_api)
api.add_resource(
    ReviewsList,
    '/reviews',
    endpoint='reviews'
)
api.add_resource(
    Review,
    '/reviews/<int:id>',
    endpoint='review'
)
