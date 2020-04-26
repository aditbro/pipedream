from flask import Flask
from flask_restful import Resource, Api
import container

app = Flask(__name__)
api = Api(app)

class Control(Resource):
    def get(self):
        return 'running'
    
    def post(self):
        container.terminate()
        return 'terminating'

api.add_resource(Control, '/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)