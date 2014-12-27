from flask import Flask, request
from flask.ext import restful

from energenie import switch_off, switch_on

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
api = restful.Api(app)

states = {1: 'Off'}


database = SqliteDatabase('ha.db')

class BaseModel(Model):
    class Meta:
        database = database

# the user model specifies its fields (or columns) declaratively, like django
class Lamp(BaseModel):
    lamp_name = CharField(unique=True)
    state = CharField()
    
    class Meta:
        order_by = ('lamp_name',)


class Lamps(restful.Resource):
    def get(self):
        return Lamp.objects.all()



class Lamp(restful.Resource):
    def get(self, lamp_id):
        return {'lamp_id': states.get(lamp_id)}

    def put(self, lamp_id):
        if states.get(lamp_id) == 'Off':
            states[lamp_id] == 'On'
            switch_on(lamp_id)
            logger.info('Turned lamp on')
        else:
            states[lamp_id] == 'Off'
            switch_off(lamp_id)
            logger.info('Turned lamp Off')
        return states

api.add_resource(Lamp, '/lamp/<int:lamp_id>')
api.add_resource(Lamps, '/lamps/')

if __name__ == '__main__':
    app.run("0.0.0.0", debug=True)