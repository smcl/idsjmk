import json
import time
import urllib.request
from vehicle import Vehicle

url = "https://mapa.idsjmk.cz/api/vehicles.json"


class IdsJmkClient:
    def __init__(self, config):
        self.config = config

    def _parse_response(self, response_str):
        response_json = json.loads(response_str)
        vehicles = [Vehicle(v, self.config) for v in response_json["Vehicles"]]
        return vehicles

    def begin(self):
        request_count = 0
        while request_count < (self.config.clip_length * self.config.frames_per_second):
            response_str = urllib.request.urlopen(url).read().decode("utf-8-sig")
            yield self._parse_response(response_str)
            time.sleep(self.config.time_between_captures)
            request_count += 1
