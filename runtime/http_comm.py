from flask import Flask
from flask_restful import Resource, Api
import container

app = Flask(__name__)
api = Api(app)

class Control(Resource):
    def get(self):
        status = container.get_status()
        return status
    
    def post(self):
        status = container.get_status()
        
        if(status == '2'):
            container.terminate()
            return 'terminating'
        else:
            return 'running'

api.add_resource(Control, '/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)