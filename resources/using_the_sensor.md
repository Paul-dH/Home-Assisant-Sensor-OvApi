
# Using the Sensor

There are multiple options for displaying the data collected by the sensor, I'll describe two and let the rest to your imagination:
- Standard usage (Example 1)
- Card showing (max 5) a list of departure times and delay if applicable (Example 2)


## Example 1

This example uses only the state of the sensor, this contains only the first upcoming departure:

Result:
![Example 1 Sensor](https://github.com/Paul-dH/Home-Assisant-Sensor-OvApi/resources/img/screen-1.png)

### Sensor configuration

 ```yaml
 sensor:
   - platform: ovapi
     name: Tram_6
     stop_code: '9505'
     route_code: '32009505'
 ```

### Group configuration

```yaml
  public_transport_plain:
    name: Openbaar vervoer
    entities:
      - sensor.tram_6__stop_9505
```

## Example 2

This example creates 5 sensors that can be displayed in a group.

### Sensor configuration:

```yaml
sensor:
  - platform: ovapi
    name: Tram_6
    stop_code: '9505'
    route_code: '32009505'
  - platform: template
    sensors:
      tram_6_departure1:
        friendly_name: Vertrek
        entity_id: sensor.tram_6__stop_9505
        icon_template: "{{ state_attr('sensor.tram_6__stop_9505','icon') }}"
        value_template: >
          {%- set i = 0 %}
          {%- set departure = state_attr('sensor.tram_6__stop_9505','departures')[i] if state_attr('sensor.tram_6__stop_9505','departures')[i] is defined else None %}
          {%- if departure %}
            {%- set message = ' - Vertraging: %s'%departure['Delay'] if departure['Delay'] | int > 0 else '' %}
            {{ departure['TargetDepartureTime'] }}{{ message }}
          {%- else %}
            Nog geen gegevens
          {%- endif %}
      tram_6_departure2:
        friendly_name: Vertrek
        entity_id: sensor.tram_6__stop_9505
        icon_template: "{{ state_attr('sensor.tram_6__stop_9505','icon') }}"
        value_template: >
          {%- set i = 1 %}
          {%- set departure = state_attr('sensor.tram_6__stop_9505','departures')[i] if state_attr('sensor.tram_6__stop_9505','departures')[i] is defined else None %}
          {%- if departure %}
            {%- set message = ' - Vertraging: %s'%departure['Delay'] if departure['Delay'] | int > 0 else '' %}
            {{ departure['TargetDepartureTime'] }}{{ message }}
          {%- else %}
            Nog geen gegevens
          {%- endif %}
      tram_6_departure3:
        friendly_name: Vertrek
        entity_id: sensor.tram_6__stop_9505
        icon_template: "{{ state_attr('sensor.tram_6__stop_9505','icon') }}"
        value_template: >
          {%- set i = 2 %}
          {%- set departure = state_attr('sensor.tram_6__stop_9505','departures')[i] if state_attr('sensor.tram_6__stop_9505','departures')[i] is defined else None %}
          {%- if departure %}
            {%- set message = ' - Vertraging: %s'%departure['Delay'] if departure['Delay'] | int > 0 else '' %}
            {{ departure['TargetDepartureTime'] }}{{ message }}
          {%- else %}
            Nog geen gegevens
          {%- endif %}
      tram_6_departure4:
        friendly_name: Vertrek
        entity_id: sensor.tram_6__stop_9505
        icon_template: "{{ state_attr('sensor.tram_6__stop_9505','icon') }}"
        value_template: >
          {%- set i = 3 %}
          {%- set departure = state_attr('sensor.tram_6__stop_9505','departures')[i] if state_attr('sensor.tram_6__stop_9505','departures')[i] is defined else None %}
          {%- if departure %}
            {%- set message = ' - Vertraging: %s'%departure['Delay'] if departure['Delay'] | int > 0 else '' %}
            {{ departure['TargetDepartureTime'] }}{{ message }}
          {%- else %}
            Nog geen gegevens
          {%- endif %}
      tram_6_departure5:
        friendly_name: Vertrek
        entity_id: sensor.tram_6__stop_9505
        icon_template: "{{ state_attr('sensor.tram_6__stop_9505','icon') }}"
        value_template: >
          {%- set i = 4 %}
          {%- set departure = state_attr('sensor.tram_6__stop_9505','departures')[i] if state_attr('sensor.tram_6__stop_9505','departures')[i] is defined else None %}
          {%- if departure %}
            {%- set message = ' - Vertraging: %s'%departure['Delay'] if departure['Delay'] | int > 0 else '' %}
            {{ departure['TargetDepartureTime'] }}{{ message }}
          {%- else %}
            Nog geen gegevens
          {%- endif %}
```

### Group configuration
```yaml
public_transport:
  name: Departures Tram 6
  entities:
    - sensor.tram_6_departure1
    - sensor.tram_6_departure2
    - sensor.tram_6_departure3
    - sensor.tram_6_departure4
    - sensor.tram_6_departure5
```
