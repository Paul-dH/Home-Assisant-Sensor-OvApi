from datetime import datetime, timedelta
import voluptuous as vol
import http.client
import logging, operator, json


from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.exceptions import PlatformNotReady
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle
from homeassistant.const import (
    CONF_NAME, CONF_STOP_CODE, CONF_ROUTE_CODE)

import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)
_RESOURCE = 'v0.ovapi.nl'

ATTR_CREDITS = 'Data provided by v0.ovapi.nl'

DEFAULT_NAME = 'Line info'

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=30)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_STOP_CODE, default=CONF_STOP_CODE): cv.string,
    vol.Optional(CONF_ROUTE_CODE, default=CONF_ROUTE_CODE): cv.string,
})

async def async_setup_platform(
        hass, config, async_add_entities, discovery_info=None):

    name = config.get(CONF_NAME)
    stop_code = config.get(CONF_STOP_CODE)
    route_code = config.get(CONF_ROUTE_CODE)

    session = async_get_clientsession(hass)

    ovapi = OvApiData(stop_area_code)

    await ovapi.async_update()

    if ovapi.data is None:
        raise PlatformNotReady

    sensors = [OvApiSensor(ovapi, name, stop_code, route_code)]

    async_add_entities(sensors, True)


class OvApiSensor(Entity):
    def __init__(self, ovapi, name, stop_code, route_code):
        self.data = ovapi
        self._name = name
        self._stop_code = stop_code
        self._route_code = route_code

    @property
    def name(self):
        """Return the name of the sensor."""
        return "{} {}".format(self._name, "stop " + self._stop_code)

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return self._icon

    @property
    def destination(self):
        for line in data[stopAreaCode][routeForth]['Passes']:
            return self.data[stopAreaCode][routeForth]['Passes'][line]['DestinationName50']

    async def async_update(self):
        """Get the latest data from the OvApi."""
        await self.data.async_update()
        self.data = self.data.data


class OvApiData:
    def __init__(self, stop_area_code):
        self.resource = _RESOURCE
        self.stop_area_code = stop_area_code
        self.data = {}
        self.headers = {
            'cache-control': "no-cache",
            'accept': "application/json"
        }

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):

        try:
            response = http.client.HTTPConnection(self.resource)
            response.request("GET", "/stopareacode/" + self.stop_area_code, headers = self.headers)
            # await result = response.getresponse()
            result = response.getresponse()
            self.data = json.loads(result.read())
            self.success = True
        except:
            _LOGGER.error("Impossible to get data from OvApi")
            self.success = False
