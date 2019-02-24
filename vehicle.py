class Vehicle(object):
    def __init__(self, vehicle_json, config):
        self.Lat = 0
        self.Lng = 0
        self.Delay = 0
        self.__dict__ = vehicle_json
        self._calc_vehicle_xy(config)

    def color(self):
        if self.Delay < 0:
            return "#70a6ff"
        elif self.Delay > 5:
            return "#ff0000"

        delay_colors = [
            "#ffffff",  # 0 seconds
            "#ffdd00",  # 1 second
            "#ffbb00",  # 2 seconds
            "#ff7700",  # 3 seconds
            "#ff4400",  # 4 seconds
            "#ff8800",  # 5 seconds
        ]

        return delay_colors[self.Delay]

    def _calc_vehicle_xy(self, config):
        lat_difference = config.lat_max - config.lat_min
        lng_difference = config.lng_max - config.lng_min

        self.x = int(config.image_size * (self.Lat - config.lat_min) / lat_difference)
        self.y = config.image_size - int(
            config.image_size * (self.Lng - config.lng_min) / lng_difference
        )
