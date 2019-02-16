from dataclasses import dataclass


@dataclass
class Config:
    image_size: int
    clip_length: int
    frames_per_second: int
    time_between_captures: int
    lat_max: float
    lat_min: float
    lng_max: float
    lng_min: float
    font: str
