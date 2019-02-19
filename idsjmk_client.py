import logging
import time
import requests
from vehicle import Vehicle

url = "https://mapa.idsjmk.cz/api/vehicles.json"


class IdsJmkClient:
    def __init__(self, config):
        self.config = config

    def _parse_response(self, response_json):
        vehicles = [Vehicle(v, self.config) for v in response_json["Vehicles"]]
        logging.info("received response, parsed %d vehicles" % len(vehicles))
        return vehicles

    def begin(self):
        request_count = 0
        logging.info("starting a new batch of requests")
        while request_count < (self.config.clip_length * self.config.frames_per_second):
            response = requests.get(url)
            yield self._parse_response(response.json())
            time.sleep(self.config.time_between_captures)
            request_count += 1
