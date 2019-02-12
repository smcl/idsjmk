from datetime import datetime
import json
import math
import os
import time
import tweepy
import urllib.request
from PIL import Image, ImageDraw, ImageEnhance

image_size = 600
consumer_key = ""
consumer_secret = ""
access_token = ""
access_secret = ""

class Vehicle(object):  
    def __init__(self, vehicle_json):
        self.Lat = 0
        self.Lng = 0
        self.__dict__ = vehicle_json
        self._calc_vehicle_xy()

    def _calc_vehicle_xy(self):
        # arbitrary calculation of the city limits (based on the terminal tram stops)
        lat_max = 49.246998
        lat_min = 49.13773
        lng_max = 16.692684
        lng_min = 16.507967

        lat_difference = lat_max - lat_min
        lng_difference = lng_max - lng_min

        self.x = int(image_size * (self.Lat - lat_min) / lat_difference)
        self.y = image_size - int(image_size * (self.Lng - lng_min) / lng_difference)

def parse_response(response_str):
    response_json = json.loads(response_str)
    vehicles = [ Vehicle(v) for v in response_json["Vehicles"] ]
    return vehicles

def vehicle_color(vehicle):
    if vehicle.Delay < 0:
        return "#70a6ff"
    elif vehicle.Delay > 5:
        return "#ff0000"

    delay_colors = [
        "#ffffff", # 0 seconds
        "#ffdd00", # 1 second        
        "#ffbb00", # 2 seconds
        "#ff7700", # 3 seconds
        "#ff4400", # 4 seconds
        "#ff0000"  # 5 seconds
    ]
    
    return delay_colors[vehicle.Delay]

def splodge(draw, x, y, eX=3, eY=3, fill="white"):
    bbox =  (
        x - eX/2, 
        y - eY/2, 
        x + eX/2, 
        y + eY/2
    )
    draw.ellipse(bbox, fill=fill)

def create_image(base_img, response_json):
    vehicles = parse_response(response_json)

    # simulate a sort of motion by taking previous image, dimming it 80% before 
    # adding new positions
    img = ImageEnhance.Brightness(base_img).enhance(0.8)
    draw = ImageDraw.Draw(img)

    # fill in vehicle colours based on how delayed they are
    for vehicle in vehicles:
        splodge(draw, vehicle.x, vehicle.y, fill=vehicle_color(vehicle))

    return img

url = "https://mapa.idsjmk.cz/api/vehicles.json"
capture_delay = 12
fps = 30
clip_length = 10

print("capturing rate: every %d seconds" % capture_delay)
print("frame rate: %d fps" % fps)
print("clip length: %d seconds" % clip_length)

while True:
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)

    img = Image.new("RGB", (image_size, image_size), "black")
    frames = []

    while len(frames) < clip_length * fps:
        try:
            response_json = urllib.request.urlopen(url).read().decode("utf-8-sig")
            img = create_image(img, response_json)
            frames.append(img.copy())
            print(".", end="", flush=True)
            time.sleep(capture_delay)
        except:
            print("E", end="", flush=True)

    filename = "%s.gif" % datetime.now().isoformat().replace(":",".")
    print("saving %s" % filename)
    frames[0].save('./%s' % filename,
        save_all=True,
        append_images=frames[1:],
        duration=int(1000 * (1.0 / fps)),
        loop=0)
    api.update_with_media('./%s' % filename)