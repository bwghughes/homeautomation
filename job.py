import datetime
import pytz
from astral import Astral

from energenie import switch_off, switch_on

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_light_outside(dawn, dusk, now=datetime.datetime.now()):
	now = pytz.utc.localize(now)
	if now > dawn and now < dusk:
		return True


def main():
	a = Astral()
	a.solar_depression = 'civil'
	city = a['Birmingham']
	timezone = city.timezone
	sun = city.sun(date=datetime.date.today(), local=True)
	if is_light_outside(sun['dawn'], sun['dusk']):
		switch_off(1)
	else:
		switch_on(1)



if __name__ == '__main__':
	main()