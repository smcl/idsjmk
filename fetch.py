import math
import time
import urllib.request

seconds = 1
minutes = 60 * seconds
hours = 60 * minutes
days = 24 * hours

url = "https://mapa.idsjmk.cz/api/vehicles.json"
#capture_every = 60 * seconds
capture_every = 5 * seconds

while True:
    filename = "first_test/%s.json" % str(math.floor(time.time()))   
    urllib.request.urlretrieve(url, filename)
    print("wrote to %s" % filename)
    time.sleep(capture_every)