from datetime import datetime
import http.client
import operator
import json

lineInfo = {}
stops = []

stopAreaCode = '9505'
routeForth = '32009505'
routeBack = '32009506'

date_format = "%Y-%m-%dT%H:%M:%S"

connection = http.client.HTTPConnection("v0.ovapi.nl")

headers = {
    'cache-control': "no-cache",
    'accept': "application/json"
    }

connection.request("GET", "/stopareacode/" + stopAreaCode, headers=headers)

result = connection.getresponse()
data = json.loads(result.read())

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