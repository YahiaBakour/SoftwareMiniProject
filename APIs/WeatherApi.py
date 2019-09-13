#pip install darksky_weather

from darksky.api import DarkSky, DarkSkyAsync
from darksky.types import languages, units, weather
import datetime, sys
sys.path.append("../")
from Config import config

apikey = config.Forecastio_API
darksky = DarkSky(apikey)

def returnWeatherData(AREA):
    forecast = darksky.get_forecast(
        AREA[0], AREA[1],
        extend=False, # default `False`
        lang=languages.ENGLISH, # default `ENGLISH`
        units=units.AUTO, # default `auto`
        exclude=[weather.MINUTELY, weather.ALERTS], # default `[]`
    )
    return (forecast.currently)

def returnWeatherDataforpast(AREA):
    forecast = darksky.get_forecast(
        AREA[0], AREA[1],
        extend=False, # default `False`
        lang=languages.ENGLISH, # default `ENGLISH`
        units=units.AUTO, # default `auto`
        exclude=[weather.MINUTELY, weather.ALERTS], # default `[]`
    )
    return (forecast.daily)

