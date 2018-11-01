## Sensor providing Public Transport information from [OVapi](http://www.ovapi.nl) in Home Assistant

This is a sensor for Home Assistant and it will retrieve departure information of a particular stop. The sensor returns a list of departure times and the reported delay.

### Install:
- Copy the ovapi.py file to: /config/custom_components/sensor/
- Add the content below to configuration.yaml:

```yaml
sensor:
  - platform: ovapi
    name: Tram_6
    stop_code: '9505'
    route_code: '32009505'
```
Above example wil only show the first upcomming departure, for more options please see: [Using the sensor](https://github.com/Paul-dH/Home-Assisant-Sensor-OvApi/blob/master/resources/using_the_sensor.md)

### To find the stop_code (stopareacode) refer to the JSON response of: [v0.ovapi.nl](http://v0.ovapi.nl/stopareacode)
I've used the building JSON parser from Firefox, the search input is on the top right.

- Search in the response with a keyword of the stop or the line you want, eg: kastelenring
- The result:
```
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

### Note and credits
- [Petro](https://community.home-assistant.io/u/petro/summary) (for extensive help at coding the template)
- [Robban](https://github.com/Kane610) - (a lot of basic help with the Python code)
- [danito](https://github.com/danito/HA-Config/blob/master/custom_components/sensor/stib.py) (I started with his script, learned a lot of it)
