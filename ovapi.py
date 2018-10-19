from datetime import datetime, timedelta
import logging, operator, json
import http.client

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (CONF_NAME)
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.exceptions import PlatformNotReady
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)
_RESOURCE = 'v0.ovapi.nl'

CONF_STOP_CODE = 'stop_code'
CONF_ROUTE_CODE = 'route_code'

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

    ovapi = OvApiData(stop_code)
    #_LOGGER.warning(ovapi)

    await ovapi.async_update()

    if ovapi is None:
        raise PlatformNotReady

    sensors = [OvApiSensor(ovapi, name, stop_code, route_code)]

    async_add_entities(sensors, True)


class OvApiSensor(Entity):
    def __init__(self, ovapi, name, stop_code, route_code):
        #self._json_data = json.dumps(ovapi, sort_keys=True, cls=JSONEncoder.encode('UTF-8')
        #self._json_data = json.dumps(ovapi, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        #self._json_data = json.dumps(ovapi)
        self._json_data = ovapi
        self._name = name
        self._stop_code = stop_code
        self._route_code = route_code

    @property
    def name(self):
        """Return the name of the sensor."""
        return "{} {}".format(self._name, "_stop_" + self._stop_code)

    @property
    def icon(self):
        return self._icon

    @property
    def destination(self):
        return self._destination

    @property
    def provider(self):
        return self._provider

    @property
    def transport_type(self):
        return self._transport_type

    @property
    def line_name(self):
        return self._line_name

    @property
    def stop_name(self):
        return self._stop_name

    async def async_update(self):
        """Get the latest data from the OvApi."""
        await self._json_data.async_update()
        self._json_data = self._json_data

        data_object = self._json_data.result.read()

        _LOGGER.warning("Debug print object: " + data_object)

        for line in data_object[self._stop_code][self._route_code]['Passes'].items():
            self._destination = data_object[self._stop_code][self._route_code]['Passes'][line]['DestinationName50']
            self._provider = data_object[self._stop_code][self._route_code]['Passes'][line]['DataOwnerCode']
            self._transport_type = data_object[self._stop_code][self._route_code]['Passes'][line]['TransportType'].title()
            self._line_name = self._transport_type + ' ' + data_object[self._stop_code][self._route_code]['Passes'][line]['LinePublicNumber'] + ' - ' + self._destination
            self._stop_name = data_object[self._stop_code][self._route_code]['Passes'][line]['TimingPointName']

        if self._transport_type == "TRAM":
            self._icon = 'mdi:train'
        if self._transport_type == "BUS":
            self._icon = 'mdi:bus'
        if self._transport_type == "METRO":
            self._icon = 'mdi:subway-variant'

class OvApiData:
    def __init__(self, stop_code):
        self.resource = _RESOURCE
        self.stop_code = stop_code
        #self.result = None
        self.headers = {
            'cache-control': "no-cache",
            'accept': "application/json"
        }

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        try:
            response = http.client.HTTPConnection(self.resource)
            response.request("GET", "/stopareacode/" + self.stop_code, headers = self.headers)
            result = response.getresponse()
            self.result = json.loads(result.read())
            #self.response_data = json.dumps(result)
            _LOGGER.warning(self.result)
            #self.success = True
        except:
            _LOGGER.error("Impossible to get data from OvApi")
            self.result = "Impossible to get data from OvApi"

        return self.result
