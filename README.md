## Sensor providing Public Transport information from [OVapi](http://www.ovapi.nl) in Home Assistant

This is a sensor for Home Assistant and it will retrieve departure information of a particular stop. The sensor returns a list of departure times and the reported delay.

### Install:
- Copy the ovapi.py file to: /config/custom_components/sensor/
- Add the content below to configuration.yaml:

```yaml
sensor:
  - platform: ovapi
    name: Tram_6
    timing_point_code: '31000226'
    show_future_departures: 4
#    line_filter: 2, 6
```

### To find the timing_point_code refer to the JSON response of: [v0.ovapi.nl](http://v0.ovapi.nl/stopareacode)
Search youre bus or tram line number, LinePublicNumber":"23" where 23 correspondents to the actual tram/bus number.
Then copy the whole entry to a temp text file:<br />
```"RET_48_1":{"LineWheelchairAccessible":"UNKNOWN","TransportType":"TRAM","DestinationName50":"Marconiplein","DataOwnerCode":"RET","DestinationCode":"TMCP---","LinePublicNumber":"23","LinePlanningNumber":"48","LineName":"Beverwaard - Marconiplein","LineDirection":1}"```

You can see here that RET_48_1 is the number we are searching for.
Now we can find the right TimingPointCode, first we will request all the tram/bus stops for the line number, go to: refer to the JSON response of: v0.ovapi.nl/line/RET_48_1 (replace with youre id)

Use Search and find the bus stop name youre leaving from, in my example it is, Beverwaardseweg.<br />
```:{"Longitude":4.5733643,"Latitude":51.898308,"TimingPointTown":"Rotterdam","TimingPointName":"Limbrichthoek","TimingPointCode":"31000226","StopAreaCode":"406","TimingPointWheelChairAccessible":"ACCESSIBLE","TimingPointVisualAccessible":"NOTACCESSIBLE","IsTimingStop":false,"UserStopOrderNumber":2},"3":```

In this line you will find the TimingPointCode ("TimingPointCode":"31000226")

Save that TimingPointCode for creating the sensor.

```Sensor example```
<pre>
cards:
  - card:
      columns: 5
      entities:
        - entity: sensor.tram_23
          icon: 'mdi:tram'
        - entity: sensor.tram_23_future_1
          icon: 'mdi:x'
        - entity: sensor.tram_23_future_2
          icon: 'mdi:x'
        - entity: sensor.tram_23_future_3
          icon: 'mdi:x'
        - entity: sensor.tram_23_future_4
          icon: 'mdi:x'
      show_header_toggle: false
      show_name: false
      title: Tram 23
      type: glance
    cards: null
    style:
      background-image: url(/local/tram.png?v=0.5)
    type: 'custom:card-modder'
  - card:
      columns: 5
      entities:
        - entity: sensor.bus_140
          icon: 'mdi:bus'
        - entity: sensor.bus_140_future_1
          icon: 'mdi:x'
        - entity: sensor.bus_140_future_2
          icon: 'mdi:x'
        - entity: sensor.bus_140_future_3
          icon: 'mdi:x'
        - entity: sensor.bus_140_future_4
          icon: 'mdi:x'
      show_header_toggle: false
      show_name: false
      title: Bus 140
      type: glance
    cards: null
    style:
      background-image: url(/local/bus1.png?v=0.2)
    type: 'custom:card-modder'
  - card:
      columns: 5
      entities:
        - entity: sensor.bus_183
          icon: 'mdi:bus'
        - entity: sensor.bus_183_future_1
          icon: 'mdi:x'
        - entity: sensor.bus_183_future_2
          icon: 'mdi:x'
        - entity: sensor.bus_183_future_3
          icon: 'mdi:x'
        - entity: sensor.bus_183_future_4
          icon: 'mdi:x'
      show_header_toggle: false
      show_name: false
      title: Bus 183
      type: glance
    cards: null
    style:
      background-image: url(/local/bus2.png?v=0.3)
    type: 'custom:card-modder'
type: vertical-stack
</pre>

### Note and credits
- [Petro](https://community.home-assistant.io/u/petro/summary) - For extensive help at coding the template.
- [Robban](https://github.com/Kane610) - A lot of basic help with the Python code.
- [Danito](https://github.com/danito/HA-Config/blob/master/custom_components/sensor/stib.py) - I started with his script, learned a lot of it)
