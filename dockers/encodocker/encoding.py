import os, logging, ffmpeg
from flask_restful import Resource, reqparse
from flask import make_response, request
from flask_jsonpify import jsonify
import receive

logging.getLogger().setLevel(logging.INFO)

            

# Lancement de la conversion
#checkDefinition(height)

class Encoding(Resource):
    def calculDef(self, file):

        input_file = file
        probe = ffmpeg.probe(input_file)
        outputName = ''

        definition = [1080, 720, 480, 360, 240]
        ratio = [120, 80, 160, 40, 80]

        # Récupération des infos de la videeo originale pour les opérations
        width = 0
        height = 0

        for metadata in probe['streams']:
            for (key, value) in metadata.items():
                #print("X :: {} \t Y :: {} \n".format(key, value))
                if key == "width":
                    width = value
                if key == "height":
                    height = value

    def conversion(input_file, width, height, outputName):

        if width != 0 and height != 0:
            os.system("ffmpeg -i {} -vf scale={}:{} -hide_banner {}.mp4".format(input_file, width, height, inputFileName+outputName))
    

    def checkDefinition(self, height, input_file):
        startIndex = 0

        #Récupère l'index de départ par rapport à la vidéo input
        for i in range(len(definition)):
            if definition[i] == height:
                startIndex = i
                break

        #Lance les copies de vidéos dans les résolutions plus basse        
        for value in range(startIndex-1, len(ratio)):
            quotient = ratio[value]
            outputName = str(definition[value])+'p'

            newWidth = 4 * quotient if definition[value] == 480 or definition[value] == 240 else 16 * quotient
            newHeight = 3 * quotient if definition[value] == 480 or definition[value] == 240 else 9 * quotient

            conversion(input_file, newWidth, newHeight, outputName)

    def post(self, file_source):

        logging.info("\nLogging the result :: {}\n\t of type :: {}".format(file_source, type(file_source)))

        # Récupération des arguments de requête
        # parser = reqparse.RequestParser()
        # parser.add_argument('file', type = str, help = "file path")
        # args = parser.parse_args()


        # Need to send a stream message to unlock the other way
        #return make_response(jsonify({'message': 'ok', 'value': args['file']}))
        
        # Formattage des data
        #completePath = args['file']

        #return 1
        completePath = file_source
        file = completePath.split('/')[-1]
        fileName = file.split('.')[0]

        # Path where videos will be store
        path = '/home/videos/'+fileName+"/"

        logging.info("\n\nPRINTING STORAGE PATH :: {}\n\n".format(path))
        
        probe = ffmpeg.probe(file_source)

        outputName = ''

        definition = [1080, 720, 480, 360, 240]
        ratio = [120, 80, 160, 40, 80]

        # Récupération des infos de la videeo originale pour les opérations
        width = 0
        height = 0

        for metadata in probe['streams']:
            for (key, value) in metadata.items():
                #print("X :: {} \t Y :: {} \n".format(key, value))
                if key == "width":
                    width = value
                if key == "height":
                    height = value
    
        startIndex = 0

        #Récupère l'index de départ par rapport à la vidéo input
        for i in range(len(definition)):
            if definition[i] == height:
                startIndex = i
                break

        #Lance les copies de vidéos dans les résolutions plus basse        
        for value in range(startIndex, len(ratio)):
            quotient = ratio[value]
            outputName = fileName+"_"+str(definition[value])+'p.mp4'

            newWidth = 4 * quotient if definition[value] == 480 or definition[value] == 240 else 16 * quotient
            newHeight = 3 * quotient if definition[value] == 480 or definition[value] == 240 else 9 * quotient

            if not os.path.exists(path):
                os.mkdir(path)


            logging.info("\n\nVIDEO PATH :: {}\n\n".format(path+outputName))

            # Basic concatenation
            file_path = path+outputName

            # Sending message to record the encoded video path
            #receiver = receive.Consumer()
            #receiver.responseQueue(file_path)
            
            if width != 0 and height != 0:
                    (
                        ffmpeg.input(file_source)
                        .filter('scale', w=newWidth, h=newHeight)
                        .output(file_path,
                                format='mp4',
                                vcodec='libx264',
                                crf=18,
                                preset='veryslow',
                                acodec='copy')
                        .overwrite_output()
                        .run()
                    )



        # Send the mail


                #logging.info("\nTest index :: {}\t printing definition :: {}\t and value :: {}\n".format(startIndex, definition[startIndex], value))
                #os.system("ffmpeg -i {} -vf scale={}:{} -hide_banner {}.mp4".format(file_source, newWidth, newHeight, path+outputName))
            
        #return make_response(jsonify({'message': 'ok', 'value': args['file']}))

        #return make_response(jsonify({'message': ' OK', 'Method': 'POST'}))