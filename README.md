# Work in progress !!

## Public Transport information from [OVapi](http://www.ovapi.nl) for Home Assistant

A sensor for Home Assistant that creates sensors containing departure information of a particular stop. The sensor returns a list of departure times and the reported delay.

The sensor can be installed as follows:
- Copy the ovapi.py file to: custom_components/sensor/
- Add the content below to configuration.yaml:

```yaml
sensor:
  - platform: ovapi
    stop_code: 9505
    route_code: 32009505
```

### To find the stop_code (stopareacode) refer to the JSON respons of: [v0.ovapi.nl](http://v0.ovapi.nl/stopareacode)
> (tip) I've used the building JSON parser from Firefox, the search input is on the top right.
- Search in the respons to a keyword of the stop or line you want, eg: kastelenring
The result
```
9505:     <-- is the stop
    TimingPointName	"Kastelenring"
```
- Browse the following url http://v0.ovapi.nl/stopareacode/9505 (replace 9505 with the code you've found!)
- minimize the child keys beneath your stop_code, there should be two returned (these are the route fourh and back).
- Open one of the keys and browse to stop_code/route_code/Passes
- This key holds all the stops currently available (this updates frequently)
- Open one of the stops
- Look for the key 'DestinationName50', this should hold the destination that you want. If this is the wrong way, then you should close the JSON output and open the other route code key.
- Note the route_code and the stop_code and place these values in the sensor connfiguration.

This repro holds a couple of files:
- README.md (this file containing the documentation)
- example.py (example script without all the Home Assistant code)
- ovapi.py (the script for Home Assistant)

Since I'm new to coding in Python I've took a lot of code from [danito](https://github.com/danito/HA-Config/blob/master/custom_components/sensor/stib.py)
