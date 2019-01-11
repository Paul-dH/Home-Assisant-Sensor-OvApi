from datetime import datetime, timedelta
import logging
import operator
import json
import itertools
import http.client

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (CONF_NAME, STATE_UNKNOWN)
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.exceptions import PlatformNotReady
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

import homeassistant.helpers.config_validation as cv

__version__ = '1.1.0'

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
ATTR_DEPARTURE = 'departure'
ATTR_DELAY = 'delay'
ATTR_DEPARTURES = 'departures'
ATTR_UPDATE_CYCLE = 'update_cycle'
ATTR_CREDITS = 'credits'

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=60)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_STOP_CODE, default=CONF_STOP_CODE): cv.string,
    vol.Optional(CONF_ROUTE_CODE, default=CONF_ROUTE_CODE): cv.string,
    vol.Optional(CONF_DATE_FORMAT, default=DEFAULT_DATE_FORMAT): cv.string,
})


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):

    name = config.get(CONF_NAME)
    stop_code = config.get(CONF_STOP_CODE)
    route_code = config.get(CONF_ROUTE_CODE)

    async_get_clientsession(hass)

    ov_api = OvApiData(stop_code)

    await ov_api.async_update()

    if ov_api is None:
        raise PlatformNotReady

    sensors = [OvApiSensor(ov_api, name, stop_code, route_code)]

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
        self._departure = None
        self._delay = None
        self._departures = None
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

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
    def departure(self):
        return self._departure

    @property
    def delay(self):
        return self._delay

    @property
    def departures(self):
        return self._departures

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
            ATTR_DEPARTURE: self._departure,
            ATTR_DELAY: self._delay,
            ATTR_DEPARTURES: self._departures,
            ATTR_UPDATE_CYCLE: str(MIN_TIME_BETWEEN_UPDATES.seconds) + ' seconds',
            ATTR_CREDITS: CONF_CREDITS
        }

    async def async_update(self):
        """Get the latest data from the OvApi."""
        await self._json_data.async_update()

        data = json.loads(self._json_data.result)

        for item in data[self._stop_code][self._route_code]['Passes'].values():
            self._destination = item['DestinationName50']
            self._provider = item['DataOwnerCode']
            self._transport_type = item['TransportType'].title()
            self._line_name = self._transport_type + ' ' + item['LinePublicNumber'] + ' - ' + self._destination
            self._stop_name = item['TimingPointName']

        stops_list = []
        for stop in itertools.islice(data[self._stop_code][self._route_code]['Passes'].values(), 5):
            stops_item = {}
            target_departure_time = datetime.strptime(stop['TargetDepartureTime'], "%Y-%m-%dT%H:%M:%S")
            expected_arrival_time = datetime.strptime(stop['ExpectedDepartureTime'], "%Y-%m-%dT%H:%M:%S")
            calculate_delay = expected_arrival_time - target_departure_time
            delay = round(calculate_delay.seconds / 60)
            stops_item["TargetDepartureTime"] = target_departure_time.time()
            stops_item["ExpectedArrivalTime"] = expected_arrival_time.time()
            stops_item["Delay"] = delay
            stops_list.append(stops_item)

        if data is None:
            self._departure = STATE_UNKNOWN
            self._delay = STATE_UNKNOWN
            self._departures = STATE_UNKNOWN
            self._state = STATE_UNKNOWN
        else:
            if stops_list is None:
                self._departure = STATE_UNKNOWN
                self._delay = STATE_UNKNOWN
                self._departures = STATE_UNKNOWN
                self._state = STATE_UNKNOWN
            else:
                stops_list.sort(key=operator.itemgetter('TargetDepartureTime'))
                self._departure = stops_list[0]["TargetDepartureTime"].strftime('%H:%M')
                self._delay = str(stops_list[0]["Delay"])

                departure_list = []
                next_stops_list = stops_list[1:]

                for counter, stop in enumerate(next_stops_list):
                    if next_stops_list[counter]["Delay"] == 0:
                        departure_list.append(next_stops_list[counter]["TargetDepartureTime"].strftime('%H:%M'))
                    else:
                        departure_list.append(next_stops_list[counter]["TargetDepartureTime"].strftime('%H:%M') +
                                              " + " + str(next_stops_list[counter]["Delay"]) + " min")
                self._departures = departure_list

                if stops_list[0]["Delay"] == 0:
                    self._state = self._departure
                else:
                    self._state = stops_list[0]["ExpectedArrivalTime"].strftime('%H:%M')

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
        self.result = ""
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
            self.result = result.read().decode('utf-8')
        except http.client.HTTPException:
            _LOGGER.error("Impossible to get data from OvApi")
            self.result = "Impossible to get data from OvApi"
