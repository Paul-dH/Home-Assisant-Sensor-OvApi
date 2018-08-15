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
ATTR_STOP_NAME = 'Stop name'
ATTR_STOPS = 'Line stops'
ATTR_ATTRIBUTION = 'Data provided by v0.ovapi.nl'

SCAN_INTERVAL = timedelta(seconds=30)
CONF_STOP_CODE = 'stop_code'
CONF_ROUTE_CODE = 'route_code'
DEFAULT_NAME = 'OvApi'
ICON = 'mdi:bus'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_STOP_CODE, 'stop_code'):
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

# ------------------------------------------------------------------------------------
#  Global script execution
# ------------------------------------------------------------------------------------

def setup_platform(hass, config, add_devices, discovery_info=None):
    sensors = []
    stations_list = set(config.get(CONF_STOP_LIST, []))

    add_devices(sensors, True)



# ------------------------------------------------------------------------------------
#  Functions
# ------------------------------------------------------------------------------------

class StibSensor(Entity):
    def __init__(self, stop, line, data, name):
        self._stop = stop
    
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
                ATTR_STOP_NAME: self._stop_name,
                ATTR_STOPS: self._stops,
            }

    @property
    def icon(self):
        if self._mode is not None:
            if self._mode == 'B':
                return 'mdi:bus'
        return ICON
    
    def update(self):
        self._data.update()

class StibData(object):
    def __init__(self, stop):
        self.stop = stop
        self.stop_data = {}

    def update(self):
        response = requests.get(_RESOURCE, params  = {'halt': self.stop})

    
    self.stop_data = stop_waiting_times 