from flask import Flask
from flask.ext import restful

from energenie import switch_off, switch_on

app = Flask(__name__)
api = restful.Api(app)

class Lamp(restful.Resource):
    def get(self, lamp_id):
        return {'lamp_id': lamp_id}

     def put(self, lamp_id):
        lamp_id = request.form['data'].get('lamp_id')
        return {'status': 'OK'}

api.add_resource(Lamp, '/lamp/<string:lamp_id>')

if __name__ == '__main__':
    app.run(debug=True)