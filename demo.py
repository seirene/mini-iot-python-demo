import sys
import matplotlib.pyplot as plt
from influxdb import InfluxDBClient
from datetime import *

hostName = 'localhost'
if len(sys.argv) > 1:
    hostName = sys.argv[1]

client = InfluxDBClient(hostName, 8086, '', '', 'mini-iot')
result = client.query('select * from temperature group by source order by time desc limit 100;')
valuesRed = list(result.get_points(measurement='temperature', tags={'source': 'red'}))
valuesBlue = list(result.get_points(measurement='temperature', tags={'source': 'blue'}))

timeFormat = "%Y-%m-%dT%H:%M:%SZ"
xsRed = [datetime.strptime(value['time'], timeFormat) for value in valuesRed]
ysRed = [value['value'] for value in valuesRed]
xsBlue = [datetime.strptime(value['time'], timeFormat) for value in valuesBlue]
ysBlue = [value['value'] for value in valuesBlue]

fig, ax = plt.subplots()
ax.set_title('Recent temperatures')
plt.plot(xsRed, ysRed, 'r')
plt.plot(xsBlue, ysBlue, 'b')
plt.xticks(rotation='vertical')
plt.tight_layout()
plt.show()
