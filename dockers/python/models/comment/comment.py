import logging
from flask import request, make_response, jsonify
from flask_restful import Resource,  reqparse
from models.comment import model as mod
import error
import include

comment_schema = mod.CommentSchema()
comments_schema = mod.CommentSchema(many=True)


class Comments(Resource):
    def get(self, video_id):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=str)
        parser.add_argument('perPage', type=str)
        args = parser.parse_args()

        _page = int(args['page']) if args['page'] and args['page'] is not "0" and args['page'].isdigit() else 1
        _perPage = int(args['perPage']) if args['perPage'] and args['perPage'] is not "0" and args[
            'perPage'].isdigit() else 50

        start_index = _perPage * _page - _perPage

        list = []

        all_comments = mod.Comment.query.filter_by(video_id=video_id).all()
        if all_comments is not None:
            result = comments_schema.dump(all_comments)
            result = result.data[start_index:start_index + _perPage]
            for row in result:
                listTmp = {
                    'id': row['id'],
                    'body': row['body'],
                    'user': include.get_user_by_id(row['user_id'])
                }
                list.append(listTmp)
            return make_response(
                jsonify({'Message ': 'OK', 'data': list, 'pager': {'current': _page, 'total': len(result)}}))
        else:
            return error.badRequest(10005)


class CreateComments(Resource):
    def post(self, video_id):
        if error.ifId_video(video_id) is False:
            return error.notFound()
        token_head = include.header()
        if error.ifToken(token_head) is True:
            parser = reqparse.RequestParser()
            parser.add_argument('body', type=str, help='Body to create comment')
            args = parser.parse_args()

            _commentBody = args['body']

            _userId = include.get_user_id_by_token(token_head)
            if _commentBody is not None and _commentBody is not "":
                new_comment = mod.Comment(_commentBody, _userId, video_id)
                mod.db.session.add(new_comment)
                mod.db.session.commit()
                result = comment_schema.dump(new_comment).data
                return make_response(CommentById.get(self, str(result['id'])), 201)
            else:
                return error.badRequest(10001, "Veuillez remplir tous les champs obligatoire!")
        else:
           return error.unauthorized()


class CommentById(Resource):
    def get(self, comment_id):
        if error.ifId_comment(comment_id) == False:
            return error.notFound()
        com = mod.Comment.query.get(comment_id)
        if com is not None:
            data = comment_schema.dump(com).data
            return make_response(jsonify({'Message': 'OK', 'data': data, 'user': include.get_user_by_id(data['user_id'])}))
        else:
            return error.notFound()


