
import os
import json

postreqdata = json.loads(open(os.environ['req']).read())
response = open(os.environ['res'], 'w')
# req = {
#   'appname' : postreqdata['appname'],
#   'boardname' :  postreqdata['boadname'],
#   'maincontact' :  postreqdata['maincontact']
#}

#json_str = json.dumps(data)
#response.write(json_str)

#response.write("appname:"['appname'] + "boardname:"['boardname'])
#apname = ['appname']

response.write("appname:"['appname'] + "boardname:"['boardname'])

response.close()