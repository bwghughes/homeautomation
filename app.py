from flask import Flask, request
from flask.ext import restful

try:
    from energenie import switch_off, switch_on
except Exception:
    pass


import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from peewee import *

app = Flask(__name__)
api = restful.Api(app)

database = SqliteDatabase('ha.db')

class BaseModel(Model):
    class Meta:
        database = database

class Lamp(BaseModel):
    lamp_name = CharField(unique=True)
    state = CharField()
    
    class Meta:
        order_by = ('lamp_name',)


class Lamps(restful.Resource):
    def get(self):
        return Lamp.objects.all()



class LampResource(restful.Resource):
    def get(self, lamp_id):
        return {'lamp_id': states.get(lamp_id)}

    def put(self, lamp_id):
        lamp = Lamp.get(Lamp.id == lamp_id)
        if lamp.state == 'Off':
            switch_on(lamp_id)
            logger.info('Turned lamp on')
            lamp.state = 'On'
            lamp.save()
        else:
            switch_off(lamp_id)
            logger.info('Turned lamp Off')
            lamp.state = 'Off'
            lamp.save()
        return '', 200

api.add_resource(LampResource, '/lamp/<int:lamp_id>')

if __name__ == '__main__':
    Lamp.create_tables(fail_silently=True)
    labels = ['Dining Room', 'Kitchen', 'Lounge']
    for x in xrange(3):
        Lamp.create(name=labels[x], state='Off')
    app.run("0.0.0.0", debug=True)