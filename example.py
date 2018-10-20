from datetime import datetime
import http.client
import operator
import json

stop_code = '9505'
route_code = '32009506'

date_format = "%Y-%m-%dT%H:%M:%S"

connection = http.client.HTTPConnection("v0.ovapi.nl")

headers = {
    'cache-control': "no-cache",
    'accept': "application/json"
    }

connection.request("GET", "/stopareacode/" + stop_code, headers = headers)

result = connection.getresponse()
string = result.read().decode('utf-8')
data = json.loads(string)

for item in data[stop_code][route_code]['Passes'].values():
    destination = item['DestinationName50']
    provider = item['DataOwnerCode']
    transport_type = item['TransportType'].title()
    line_name = transport_type + ' ' + item['LinePublicNumber'] + ' - ' + destination
    stop_name = item['TimingPointName']

    #print(next(iter(data[stop_code][route_code]['Passes'].values())))

print(destination)
print(provider)
print(transport_type)
print(line_name)
print(stop_name)

stops = []

for stop in data[stop_code][route_code]['Passes']:

    item = {}

    TargetDepartureTime  = datetime.strptime(data[stop_code][route_code]['Passes'][stop]['TargetDepartureTime'], date_format)
    ExpectedArrivalTime  = datetime.strptime(data[stop_code][route_code]['Passes'][stop]['ExpectedDepartureTime'], date_format)
    #print("TargetDepartureTime: " + str(TargetDepartureTime) + " | ExpectedArrivalTime: " + str(ExpectedArrivalTime))

    calculateDelay = ExpectedArrivalTime - TargetDepartureTime
    #print("calculateDelay: " + str(calculateDelay))

    delay = str(round((calculateDelay.seconds) / 60))

    item["TargetDepartureTime"] = str(TargetDepartureTime.time())[0:5]
    item["Delay"] = delay

    stops.append(item)

stops.sort(key=operator.itemgetter('TargetDepartureTime'))

#print(stops)




"""
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

print(lineInfo)
"""
