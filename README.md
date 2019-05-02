## Sensor providing Public Transport information from [OVapi](http://www.ovapi.nl) in Home Assistant

This is a sensor for Home Assistant and it will retrieve departure information of a particular stop. The sensor returns the first upcomming departure.

![Lovelace Screenshot](https://github.com/Paul-dH/Home-Assisant-Sensor-OvApi/blob/master/resources/img/preview.png)

### Install:
- Create the followinf folder structure: /config/custom_components/ovapi and place these [3 files](https://github.com/Paul-dH/Home-Assisant-Sensor-OvApi/tree/master/custom_components/ovapi) there.
- Add the configuration to configuration.yaml, see the parameter descriptions below and refer to the examples.

### Sensor options (there are two ways to use the sensor):

**1. Using a stop_code:** *(Please refer to the instructions below)*
- **platform: ovapi** *(required)* - The name of the sensor component.
- **name: line_6** - The name of the sensor in HASS
- **stop_code** *(int, e.g. 9505)* - A code created by the transport to identify the stop.
- **route_code** *(int, e.g. 32009505)* - A stop always has two routes, a route forth and back. This code configures the right route that you want of a public line destination.

**2. Using a Timing_Point_Code:** *(Please refer to the instructions below)*
- **platform: ovapi** *(required)* - The name of the sensor component.
- **name: line_6** - The name of the sensor in HASS
- **timing_point_code:** *(int, e.g. 10155690)* - A code created by the transport to identify the stop.

**Either one of these are required for the sensor to function!**

**Optional parameters:**
- **show_future_departures:** *(int, max value is 50)* - The sensor always creates one sensor in Hass, this property can be configured with a value of 2-5. If this is configured, the component creates the configured number of sensors in HASS. These sensors contain future departments together with theire delay if applicable.
- **line_filter** *(int, comma seperated)* - You might bump into the fact that there are multiple lines that use the same stop, with this property you can filter all passes with the line number that you want.


### To find the stop_code (stopareacode) refer to the JSON response of: [v0.ovapi.nl](http://v0.ovapi.nl/stopareacode)
I've used the building JSON parser from Firefox, the search input is on the top right.

- Search in the response with a keyword of the stop or the line you want, eg: kastelenring
- The result:
```json
9505:    <-- is the stop
  TimingPointName "Kastelenring"
```
- Browse the following Url: http://v0.ovapi.nl/stopareacode/9505 (replace 9505 with the code you've found!)
- Minimize the child keys beneath your stop_code, two keys should be returned (these are the route fourth and back).
- Open one of the keys and browse to stop_code/route_code/Passes
- This key holds all the stops currently available (this updates frequently)
- Open one of the stops
- Look for the key 'DestinationName50', this should hold the destination that you want. If this is the wrong way, then you should close the JSON output and open the other route code key.
- Note the route_code and the stop_code and place these values in the sensor configuration.


### To find the timing_point_code (TimingPointCode) refer to the JSON response of: [v0.ovapi.nl](http://v0.ovapi.nl/line)
I've used the building JSON parser from Firefox, the search input is on the top right.

- Search in the response with a keyword of the destination of the line, eg: Leyenburg
- The result of this should be a list of line identifiers, expand them and look for the one that has the correct value in `DestinationName50`. Copy the line identifier, e.g. HTM_6_2.
- Next, open the url: [http://v0.ovapi.nl/line/HTM_6_2](http://v0.ovapi.nl/line/HTM_6_2), this page lists all stops of the line. Search for your stop name, e.g. kastelenring.
- Find the TimingPointCode and use this as value in the sensor configuration.

### Sensor configuration examples
Create 1 sensor to show the next upcomming departure of a particular line
```yaml
sensor:
  - platform: ovapi
    name: Tram_6
    stop_code: 9595
    route_code: 32009505
```

Create a base sensor and 4 future sensors, this way you can display the time of 5 departures in total
```
cards:
  - card:
      columns: 5
      entities:
        - entity: sensor.tram_23_templated
          icon: 'mdi:tram'
        - entity: sensor.tram_23_future_1_templated
          icon: 'mdi:x'
        - entity: sensor.tram_23_future_2_templated
          icon: 'mdi:x'
        - entity: sensor.tram_23_future_3_templated
          icon: 'mdi:x'
        - entity: sensor.tram_23_future_4_templated
          icon: 'mdi:x'
      show_header_toggle: false
      show_name: false
      title: Tram 23
      type: glance
    cards: null
    style:
      background-image: url(/local/images/tram.png?v=0.6)
    type: 'custom:card-modder'
  - card:
      columns: 5
      entities:
        - entity: sensor.bus_140_templated
          icon: 'mdi:bus'
        - entity: sensor.bus_140_future_1_templated
          icon: 'mdi:x'
        - entity: sensor.bus_140_future_2_templated
          icon: 'mdi:x'
        - entity: sensor.bus_140_future_3_templated
          icon: 'mdi:x'
        - entity: sensor.bus_140_future_4_templated
          icon: 'mdi:x'
      show_header_toggle: false
      show_name: false
      title: Bus 140
      type: glance
    cards: null
    style:
      background-image: url(/local/images/bus1.png?v=0.3)
    type: 'custom:card-modder'
  - card:
      columns: 5
      entities:
        - entity: sensor.bus_183_templated
          icon: 'mdi:bus'
        - entity: sensor.bus_183_future_1_templated
          icon: 'mdi:x'
        - entity: sensor.bus_183_future_2_templated
          icon: 'mdi:x'
        - entity: sensor.bus_183_future_3_templated
          icon: 'mdi:x'
        - entity: sensor.bus_183_future_4_templated
          icon: 'mdi:x'
      show_header_toggle: false
      show_name: false
      title: Bus 83 / 183
      type: glance
    cards: null
    style:
      background-image: url(/local/images/bus2.png?v=0.1)
    type: 'custom:card-modder'
type: vertical-stack

```


### Note and credits
- [Petro](https://community.home-assistant.io/u/petro/summary) - For extensive help at coding the sensor templates.
- [Robban](https://github.com/Kane610) - A lot of basic help with the Python code.
- [Danito](https://github.com/danito/HA-Config/blob/master/custom_components/sensor/stib.py) - I started with his script, learned a lot of it)
- [pippyn](https://github.com/pippyn) - Huge contributions and a lot of bugfixes, thanks mate!
- [rolfberkenbosch](https://github.com/rolfberkenbosch/) - For a start of the timing_point_code documentation.
- [IIIdefconIII](https://github.com/IIIdefconIII/) - Some minor contributions to add the custom updater and updating the readme.

### Custom updater:
```
custom_updater:
  track:
    - components
  component_urls:
    - https://raw.githubusercontent.com/Paul-dH/Home-Assisant-Sensor-OvApi/master/custom_components.json
```

