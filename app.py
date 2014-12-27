from flask import Flask, request
from flask.ext import restful

from energenie import switch_off, switch_on

app = Flask(__name__)
api = restful.Api(app)

states = {1: 'Off'}

class Lamps(restful.Resource):
    def get(self):
        return states



class Lamp(restful.Resource):
    def get(self, lamp_id):
        return {'lamp_id': states.get(lamp_id)}

    def put(self, lamp_id):
        if states.get(lamp_id) == 'Off':
            states[lamp_id] == 'On'
            switch_on(lamp_id)
        else:
            states[lamp_id] == 'Off'
            switch_off(lamp_id)
        return states

api.add_resource(Lamp, '/lamp/<int:lamp_id>')
api.add_resource(Lamps, '/lamps/')

if __name__ == '__main__':
    app.run("0.0.0.0", debug=True)