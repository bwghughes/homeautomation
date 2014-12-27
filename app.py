import time
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
    name = CharField(unique=False)
    state = CharField()
    
    class Meta:
        order_by = ('name',)


class LampsResource(restful.Resource):
    
    def put(self):
        for lamp in Lamp.select():
            if lamp.state == 'Off':
                logger.info('Turning on lamp {}.'.format(lamp.id))
                def on():
                    for x in xrange(3):
                        switch_on()
                        time.sleep(0.3)
                on()
                lamp.state = "On"
                lamp.save()
            else:
                logger.info('Turning on lamp {}.'.format(lamp.id))
                def off():
                    for x in xrange(3):
                        switch_off()
                        time.sleep(0.3)
                on()
                lamp.state = "Off"
                lamp.save()
        return '', 200



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
api.add_resource(LampsResource, '/lamps/')

if __name__ == '__main__':
    Lamp.drop_table(fail_silently=True)
    Lamp.create_table(fail_silently=True)
    names = ['Dining Room', 'Kitchen', 'Lounge']
    for x in xrange(3):
        Lamp.create(name=names[x], state='Off')
    app.run("0.0.0.0", debug=True)