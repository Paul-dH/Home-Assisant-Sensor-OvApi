from datetime import datetime, timedelta
import logging, operator, json, itertools
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
CONF_DATE_FORMAT = 'date_format'
CONF_CREDITS = 'Data provided by v0.ovapi.nl'

DEFAULT_NAME = 'Line info'
DEFAULT_DATE_FORMAT = "%y-%m-%dT%H:%M:%S"

ATTR_NAME = 'name'
ATTR_STOP_CODE = 'stop_code'
ATTR_ROUTE_CODE = 'route_code'
ATTR_ICON = 'icon'
ATTR_DESTINATION = 'destination'
ATTR_PROVIDER = 'provider'
ATTR_TRANSPORT_TYPE = 'transport_type'
ATTR_LINE_NAME = 'line_name'
ATTR_STOP_NAME = 'stop_name'
ATTR_CREDITS = 'credits'

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=15)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_STOP_CODE, default=CONF_STOP_CODE): cv.string,
    vol.Optional(CONF_ROUTE_CODE, default=CONF_ROUTE_CODE): cv.string,
    vol.Optional(CONF_DATE_FORMAT, default=DEFAULT_DATE_FORMAT): cv.string,
})

async def async_setup_platform(
        hass, config, async_add_entities, discovery_info=None):

    name = config.get(CONF_NAME)
    stop_code = config.get(CONF_STOP_CODE)
    route_code = config.get(CONF_ROUTE_CODE)

    session = async_get_clientsession(hass)

    ovapi = OvApiData(stop_code)

    await ovapi.async_update()

    if ovapi is None:
        raise PlatformNotReady

    sensors = [OvApiSensor(ovapi, name, stop_code, route_code)]

    async_add_entities(sensors, True)


class OvApiSensor(Entity):
    def __init__(self, ovapi, name, stop_code, route_code):
        self._json_data = ovapi
        self._name = name
        self._stop_code = stop_code
        self._route_code = route_code
        self._icon = None
        self._destination = None
        self._provider = None
        self._transport_type = None
        self._line_name = None
        self._stop_name = None
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return "{} {}".format(self._name.strip(), "_stop_" + self._stop_code)

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

    @property
    def state(self):
        return self._state

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return{
            ATTR_NAME: self._name,
            ATTR_STOP_CODE: self._stop_code,
            ATTR_ROUTE_CODE: self._route_code,
            ATTR_ICON: self._icon,
            ATTR_DESTINATION: self._destination,
            ATTR_PROVIDER: self._provider,
            ATTR_TRANSPORT_TYPE: self._transport_type,
            ATTR_LINE_NAME: self._line_name,
            ATTR_STOP_NAME: self._stop_name,
            ATTR_CREDITS: CONF_CREDITS
        }

    async def async_update(self):
        """Get the latest data from the OvApi."""
        await self._json_data.async_update()

        data = json.loads(self._json_data._result)

        for item in data[self._stop_code][self._route_code]['Passes'].values():
            self._destination = item['DestinationName50']
            self._provider = item['DataOwnerCode']
            self._transport_type = item['TransportType'].title()
            self._line_name = self._transport_type + ' ' + item['LinePublicNumber'] + ' - ' + self._destination
            self._stop_name = item['TimingPointName']

        stops_list = []
        for stop in itertools.islice(data[self._stop_code][self._route_code]['Passes'].values(), 5):

            stops_item = {}

            TargetDepartureTime  = datetime.strptime(stop['TargetDepartureTime'], "%Y-%m-%dT%H:%M:%S")
            ExpectedArrivalTime  = datetime.strptime(stop['ExpectedDepartureTime'], "%Y-%m-%dT%H:%M:%S")

            calculateDelay = ExpectedArrivalTime - TargetDepartureTime

            delay = str(round((calculateDelay.seconds) / 60))

            stops_item["TargetDepartureTime"] = str(TargetDepartureTime.time())[0:5]
            stops_item["Delay"] = delay

            stops_list.append(stops_item)

        stops_list.sort(key=operator.itemgetter('TargetDepartureTime'))

        self._state = json.dumps(stops_list).replace(" ", "")

        if self._transport_type == "Tram":
            self._icon = 'mdi:train'
        if self._transport_type == "Bus":
            self._icon = 'mdi:bus'
        if self._transport_type == "Metro":
            self._icon = 'mdi:subway-variant'

class OvApiData:
    def __init__(self, stop_code):
        self._resource = _RESOURCE
        self._stop_code = stop_code
        self._headers = {
            'cache-control': "no-cache",
            'accept': "application/json"
        }

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        try:
            response = http.client.HTTPConnection(self._resource)
            response.request("GET", "/stopareacode/" + self._stop_code, headers = self._headers)
            result = response.getresponse()
            self._result = result.read().decode('utf-8')
        except:
            _LOGGER.error("Impossible to get data from OvApi")
            self._result = "Impossible to get data from OvApi"
