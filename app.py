from flask import Flask
from flask.ext import restful

from energenie import switch_off, switch_on

app = Flask(__name__)
api = restful.Api(app)

states = {1: 'Off'}

class Lamp(restful.Resource):
    def get(self, lamp_id):
        return {'lamp_id': states.get(lamp_id)}

    def put(self, lamp_id):
        lamp_id = int(request.form['data'].get('lamp_id'))
        if states.get(lamp_id) == 'Off':
            states[lamp_id] == 'On'
            switch_on(lamp_id)
        return states

api.add_resource(Lamp, '/lamp/<string:lamp_id>')

if __name__ == '__main__':
    app.run("0.0.0.0", debug=True)