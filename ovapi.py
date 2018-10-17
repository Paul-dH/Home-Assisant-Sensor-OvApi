from datetime import datetime, timedelta
import voluptuous as vol
import http.client
import operator
import logging
import json

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle
from homeassistant.const import CONF_NAME, ATTR_ATTRIBUTION, STATE_UNKNOWN
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

_RESOURCE = 'v0.ovapi.nl'

ATTR_DESTINATION = 'Destination'
ATTR_PROVIDER = 'Transport company'
ATTR_TRANSPORT_TYPE = 'Transport Type'
ATTR_LINE_NAME = 'Line name'
ATTR_LINE_NUMBER = 'Line number'
ATTR_STOP_NAME = 'Stop name'
ATTR_ATTRIBUTION = 'Data provided by v0.ovapi.nl'

SCAN_INTERVAL = timedelta(seconds=30)
CONF_ROUTE_CODES_LIST = 'line ids'
CONF_ROUTE_CODE = 'route_code'
DEFAULT_NAME = 'OvApi'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_LINE_LIST, 'line_filter'):
            vol.All(
                cv.ensure_list,
                vol.Length(min=1),
                [cv.string]),
    vol.Optional(CONF_ROUTE_CODE, 'route_code'):
            vol.All(
                cv.ensure_list,
                vol.Length(min=1),
                [cv.string]),
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    sensors = []
    line_list = set(config.get(CONF_LINE_LIST, []))
    url = _RESOURCE
    interval = SCAN_INTERVAL
    for line in line_list:
       d = StibData(station)
       d.update()
       data = d.stop_data
       lines = data['lines']
       stop_name = data["stop_name"][0].replace("-", "_").replace(" ","_")
       for l in lines:
           line = lines[l][0]['line']
           sensors.append(StibSensor(station, line, d, stop_name))

    add_devices(sensors, True)

class StibSensor(Entity):
    def __init__(self, stop_code, line_name, line_number, line_data):
        self.destination = None
        self.provider = None
        self.transport_type = None
        self.line_name = None
        self.line_number = line_number
        self.line_data = line_data
        self.stop_name = None
        self.stop_code = stop_code
        self.stops = None
        self._state = STATE_UNKNOWN

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def device_state_attributes(self):
        if self._data is not None:
            return {
                ATTR_DESTINATION: self._destination,
                ATTR_PROVIDER: self._provider,
                ATTR_TRANSPORT_TYPE: self._transport_type,
                ATTR_LINE_NAME: self._line_name,
                ATTR_LINE_NUMBER: self._line_number,
                ATTR_STOP_NAME: self._stop_name,
                ATTR_STOPS: self._stops,
            }

    @property
    def icon(self):
        if self._mode is not None:
            if self.transporttype == 'BUS':
                return 'mdi:bus'
            if self.transporttype == 'TRAM':
                return 'mdi:tram'
            if self.transporttype == 'METRO':
                return 'mdi:subway'
        return ICON

    def update(self):
        self._data.update()

class StibData(object):
    def __init__(self, stop):
        self.date_format = "%Y-%m-%dT%H:%M:%S"
        self.stop_area_code = CONF_STOP_CODE
        self.route_code = CONF_ROUTE_CODE
        self.return_data = {}

    def update(self):
        line_info = {}
        stops = []

        headers = {
            'cache-control': "no-cache",
            'accept': "application/json"
        }

        response = http.client.HTTPConnection(_RESOURCE)
        response.request("GET", "/stopareacode/" + stop_area_code, headers=headers)
        result = response.getresponse()
        data = json.loads(result.read())

        if data:
            for line in data[stopAreaCode][routeForth]['Passes']:

                lineInfo["Destination"] = data[stopAreaCode][routeForth]['Passes'][line]['DestinationName50']
                lineInfo["Provider"] = data[stopAreaCode][routeForth]['Passes'][line]['DataOwnerCode']
                lineInfo["TransportType"] = data[stopAreaCode][routeForth]['Passes'][line]['TransportType'].title()
                lineInfo["LineName"] = lineInfo['TransportType'] + ' ' + data[stopAreaCode][routeForth]['Passes'][line]['LinePublicNumber'] + ' - ' + lineInfo["Destination"]
                lineInfo["StopName"] = data[stopAreaCode][routeForth]['Passes'][line]['TimingPointName']

                lineInfo["Stops"] = stops

            for stop in data[stopAreaCode][routeForth]['Passes']:

                item = {}

                TargetDepartureTime  = datetime.strptime(data[stopAreaCode][routeForth]['Passes'][stop]['TargetDepartureTime'], date_format)
                ExpectedArrivalTime  = datetime.strptime(data[stopAreaCode][routeForth]['Passes'][stop]['ExpectedDepartureTime'], date_format)

                calculateDelay = ExpectedArrivalTime - TargetDepartureTime

                delay = str(round((calculateDelay.seconds) / 60))

                item["TargetDepartureTime"] = str(TargetDepartureTime.time())[0:5]
                item["Delay"] = delay

                stops.append(item)
            stops.sort(key=operator.itemgetter('TargetDepartureTime'))

        else:
            _LOGGER.error("Impossible to get data from OvApi. Response code: %s. Check %s", response.status_code, response.url)
            line_info = None

    self.return_data = line_info
