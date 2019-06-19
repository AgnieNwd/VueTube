import logging
from flask import request, make_response, jsonify, redirect, url_for
from flask_restful import Resource,  reqparse
from models.video import model as mod
import error
import include
import upload
import requests
import config

video_schema = mod.VideoSchema()
videos_schema = mod.VideoSchema(many=True)

logging.getLogger().setLevel(logging.INFO)


class Videos(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('page', type=str)
        parser.add_argument('perPage', type=str)
        args = parser.parse_args()
        ## user/duration a ajouter
        _name = args['name'] if args['name'] else ''
        _page = int(args['page']) if args['page'] and args['page'] is not "0" and args['page'].isdigit() else 1
        _perPage = int(args['perPage']) if args['perPage'] and args['perPage'] is not "0" and args[
            'perPage'].isdigit() else 50

        limit = _perPage * _page - _perPage
        if _name != "":
            all_video = mod.Video.query.filter(mod.Video.name.like('%' + _name + '%')).all()
        else:
            all_video = mod.Video.query.all()
        
        result = videos_schema.dump(all_video)
        result = result.data[limit:limit + _perPage]
        list = []
        for row in result:
            listTmp = {
                'id': row['id'],
                'name': row['name'],
                'source': row['source'],
                'duration': row['duration'],
                'created_at': row['created_at'],
                'view': row['view'],
                'enabled': row['enabled'],
                'user': include.get_user_by_id(row['user_id'])
            }
            list.append(listTmp)
        return make_response(jsonify({'Message ': 'OK', 'data': list, 'pager': {'current': _page, 'total': len(result)}}))

    
class Video(Resource):
    def get(self, video_id):
        if error.ifId_video(video_id) is not False:
            video = mod.Video.query.get(video_id)
            data = video_schema.dump(video).data
            user = include.get_user_by_id(data['user_id'])
            data.update({'user': user})
            return make_response(jsonify({'Message': 'OK', 'data': data}))
        else:
            return error.notFound()

    def delete(self, video_id):
        if error.ifId_video(video_id) is False:
            return error.notFound()
        token_head = include.header()
        if error.ifToken(token_head) is True:
            if include.get_user_id_by_token(token_head) != include.get_user_id_by_video_id(video_id):
                return error.forbidden()
            include.delete_com_form_by_video_id(video_id)
            video = mod.Video.query.get(video_id)
            if video is not None:
                mod.db.session.delete(video)
                mod.db.session.commit()
                return {}, 204
            else:
                return error.badRequest(10005, "erreur dans le traitement de la requête")
        else:
            return error.unauthorized()

    def put(self, video_id):
        # TODO: enable ou pas à faire
        if error.ifId_video(video_id) is False:
            return error.notFound()
        token_head = include.header()
        if error.ifToken(token_head) is True:
            if include.get_user_id_by_token(token_head) != include.get_user_id_by_video_id(video_id):
                return error.forbidden()
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, help='Name of the video')
            parser.add_argument('enable', type=bool, action='store_true', help='The video could be watched')
            args = parser.parse_args()

            logging.info("Print ARGS :: {} \n\n".format(args))

            _name = args['name']
            _enable = error.isBool(args['enable'])

            if _name is not None and _enable is not None:
                video = mod.Video.query.get(video_id)
                if video is not None:
                    logging.info("TYPE OF :: {} \n\n".format(_enable))
                    logging.info("TYPE OF :: {} \n\n".format(type(_enable)))
                    video.name = _name
                    video.enabled = _enable
                    logging.info("TYPE OF :: {} \n\n".format(video.enabled))
                    mod.db.session.commit()
                    return self.get(video_id)
                else:
                    return error.badRequest(10005, "erreur dans le traitement de la requête")
            else:
                return error.badRequest(10001, "Merci de compléter les champs obligatoires")
        else:
            return error.unauthorized()

    """ ENCODING VIDEO """
    def patch(self, video_id):
        if error.ifId_video(video_id) is False:
            return error.notFound()
        token_head = include.header()
        if error.ifToken(token_head) is True:
            # En attendant le JWT, on fait avec le token simple !!!!
            if include.get_user_id_by_token(token_head) != include.get_user_id_by_video_id(video_id):
                return error.forbidden()
            parser = reqparse.RequestParser()
            parser.add_argument('format', type=str, help='Name of the video')
            args = parser.parse_args()

            formatVideo = args['format'] if args['format'] else '480'
            new_format = mod.VideoFormat(formatVideo, 'test uri pour le moment', video_id)
            mod.db.session.add(new_format)
            mod.db.session.commit()
            retour_video_format = mod.VideoFormatSchema().dump(new_format).data

            video = mod.Video.query.get(retour_video_format['video_id'])
            result = video_schema.dump(video).data
            logging.info("SHOW RESULT FROM VIDEO REQUEST :: {} \n\n".format(result))
            return make_response(jsonify({'Message': 'OK', 'data': result}), 201)
        else:
            return error.unauthorized()


class VideoByUser(Resource):
    def post(self, user_id):
        # TODO: Filename de la video à gerer
        if error.ifId(user_id) is False:
            return error.notFound()
        token_head = include.header()
        if error.ifToken(token_head) is True:
            id_user = include.get_user_id_by_token(token_head)

            """ user_id is received as str, so we need to cast it in int """
            if id_user != int(user_id):
                return error.forbidden()
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str, help='name of the video')
            parser.add_argument('source', type=str, help='file of the video')
            args = parser.parse_args()

            uploader = upload.Upload()

            _name = args['name']
            _source = uploader.upload_file()

            # Redirection de la requête vers la route suivante
            test = requests.get("http://localhost:5000/testing", data={'file': _source})

            # Récupère le retour de la requête au format json
            r = test.json()

            logging.info("\nMessage is :: {}\n\n".format(r))
            #logging.info("Message is :: {}".format(message))

            if test.status_code == 200:# is not None:
                #print(test)
                #x = test.json()
                #logging.info("Message :: {}".format(x))
                return r
                #return make_response(jsonify({'Message', test}))
            else:
                return "KO"
            if _name and _source is not None and _name and _source is not "":
                new_video = mod.Video(_name, 300, id_user, _source, 0, 1)
                mod.db.session.add(new_video)
                mod.db.session.commit()
                result = video_schema.dump(new_video).data
                return make_response(jsonify({'Message': 'OK', 'data': result}), 201)
            else:
                return error.badRequest(10001, "Veuillez remplir tous les champs obligatoire!")
        else:
            return error.unauthorized()


class VideosByUser(Resource):
    def get(self, user_id):
        if error.ifId(user_id) is False:
            return error.notFound()
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=str)
        parser.add_argument('perPage', type=str)
        args = parser.parse_args()

        _page = int(args['page']) if args['page'] and args['page'] is not "0" and args['page'].isdigit() else 1
        _perPage = int(args['perPage']) if args['perPage'] and args['perPage'] is not "0" and args[
            'perPage'].isdigit() else 50

        limit = _perPage * _page - _perPage
        all_video = mod.Video.query.filter_by(user_id=user_id).all()
        result = videos_schema.dump(all_video)
        result = result.data[limit:limit + _perPage]
        return make_response(jsonify({'Message ': 'OK', 'data': result, 'pager': {'current': _page, 'total': len(result)}}))

class TestReachDocker(Resource):
    def get(self):
        logging.info("WE ARE TESTING THE ROUTING")

        parser = reqparse.RequestParser()
        parser.add_argument('file', help='Will be the uploaded file')
        args = parser.parse_args()

        logging.info("\n AFFICHAGE DU PARAM REÇU :: {}\n\n".format(args))

        input_var = 5
        url = config.DOCKER_ROUTE
        logging.info("\n\n\nPrint url from server :: {} \n\n".format(url))
        input_json = {'arg':input_var}
        
        # Tests on GET
        responseGet = requests.get(url, data=input_json)
        logging.info("\n\n LOGGING POST :: \n STATUS :: {}\n REASON :: {}\n".format(responseGet.status_code, responseGet.reason))
        
        # Tests on POST
        responsePost = requests.post(url=url, data=input_json)
        test = responsePost.json()
        logging.info("\n\n LOGGING POST :: \n STATUS :: {}\n REASON :: {}\n RESPONSE :: {}\n".format(responsePost.status_code, responsePost.reason, test))

        #data = request.data

        #logging.info("\n\n\nPrint res from server :: {} \n\n".format(res))
        #logging.info("\n\n\nPrint data from server :: {} \n\n".format(truc))

        #dictFromServer = res.json()
        return make_response(jsonify(test))

        logging.info("Print dict from server :: {} \n".format(dictFromServer))
        return dictFromServer
        return dictFromServer['message']