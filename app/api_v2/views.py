import datetime
from flask import Flask, jsonify, request
from functools import wraps
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import enum
from ..post.models import Category, Posts
from ..auth.models import User
from .. import db

from . import api_v2_blueprint, api

api_id = 5
api_username = 'TonyDAngelo'
api_password = 'Caleb_konley_WithAK'


def protected(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == api_username and auth.password == api_password:
            return f(*args, **kwargs)
        return jsonify({'message': 'Authentication failed!'}), 403

    return decorated

task_post_args = reqparse.RequestParser()
task_post_args.add_argument("title", type = str, help = "Title is required", required = True)
task_post_args.add_argument("text", default = "", type = str, required = False)
task_post_args.add_argument("image_file", default = "", type = str, required = False)
task_post_args.add_argument("type", type = str, help = "Type is required", required = True)
task_post_args.add_argument("enabled", type = str, help = "Title is required", required = True)
task_post_args.add_argument("category_id", type = int, help = "Category is required", required = True)

task_update_args = reqparse.RequestParser()
task_update_args.add_argument("title", type = str, help = "Title is required", required = True)
task_update_args.add_argument("text", type = str, required = False)
task_update_args.add_argument("image_file", type = str, help = "Title is required", required = True)
task_update_args.add_argument("type", type = str, help = "Type is required", required = True)
task_update_args.add_argument("enabled", default = False, type = bool, required = False)
task_update_args.add_argument("category_id", type = int, help = "Category is required", required = True)

resource_fields = {
	'id': fields.Integer,
	'title': fields.String,
    'text': fields.String,
    'image_file': fields.String,
    'created': fields.String,
	'type': fields.String,
    'enabled': fields.Boolean,
    'user_id': fields.Integer,
    'category_id': fields.String
}

class PostsList(Resource):
    def get(self):
        posts = Posts.query.all()
        return_values =  {}
        for post in posts:
            return_values[post.id] = {"id": post.id, 
                                        "title": post.title, 
                                        "text": post.text, 
                                        "image_file": post.image_file,
                                        "created": post.created.strftime(),
                                        "type": post.type,
                                        "enabled": post.enabled,
                                        "user_id": post.user_id,
                                        "category_id": post.category_id
                                        }
        print(return_values)
        return return_values

class PostTask(Resource):
    @marshal_with(resource_fields)
    @protected
    def get(self, id):
        result = Posts.query.filter_by(id=id).first()
        if not result:
            abort(404, message="Не знайдено пост з даним id")
        return result

    @marshal_with(resource_fields)
    @protected
    def post(self, id):
        args = task_post_args.parse_args()
        result = Posts.query.filter_by(id = id).first()
        user_active = User.query.filter_by(username = api_username).first()
        if result:
            abort(409, message="Id поста використовується")
        
        if not user_active:
            abort(409, message="Аккаунт користувача відсутній")

        post = Posts(id=id, title=args['title'],
                        text=args['text'],
                        image_file = args['image_file'],
                        created = datetime.now(),
                        type = args['type'],
                        enabled = args['enabled'],
                        user_id = user_active.id,
                        category_id = args['category_id']
                        )
        db.session.add(post)
        db.session.commit()
        return post, 201 

    @marshal_with(resource_fields)
    @protected
    def put(self, id):
        args = task_update_args.parse_args()
        result = Posts.query.filter_by(id = id).first()

        if not result:
            abort(404, message="Даний пост не існує, неможливо оновити")

        user_active = User.query.filter_by(username = api_username).first()
        if user_active.id == result.user_id:
            abort(409, message="Це не пост користувача!")

        if args['title']:
            result.title = args.title
        if args['text']:
            result.text = args.text
        if args['image_file']:
            result.image_file = args.image_file
        if args['type']:
            result.type = args.type
        if args['title']:
            result.title = args.title
        if args['enabled']:
            result.enabled = args.enabled
        category_id = Category.query.filter_by(id = args['category_id'])
        if not category_id:
            abort(404, message="Не існує даної категорії")

        if args['category_id']:
            result.category_id = args.category_id
        
        db.session.commit()

        return result

    @marshal_with(resource_fields)
    @protected
    def delete(self, id):
        post = Posts.query.filter_by(id = id).first()
        user_active = User.query.filter_by(username = api_username).first()
        if user_active.id == post.user_id:
            db.session.delete(post)
            return "Пост було видалено", 204
        abort(409, message="Це не пост користувача!")

api.add_resource(PostsList, "/posts")
api.add_resource(PostTask, "/post/<int:id>")

