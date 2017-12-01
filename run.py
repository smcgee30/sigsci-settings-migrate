
import os
import json

postreqdata = json.loads(open(os.environ['req']).read())
response = open(os.environ['res'], 'w')
data = {
   'name' : postreqdata['name'],
   'shares' : 100,
   'price' : 542.23
}

json_str = json.dumps(data)
response.write(json_str)
response.close()