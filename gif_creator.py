from datetime import datetime
from PIL import Image, ImageDraw, ImageEnhance, ImageFont

# draw.point() is too tiny, so just draw a little circle using draw.ellipse()
def splodge(draw, x, y, eX=3, eY=3, fill="white"):
    bbox = (x - eX / 2, y - eY / 2, x + eX / 2, y + eY / 2)
    draw.ellipse(bbox, fill=fill)


class GifCreator:
    def __init__(self, config):
        self.config = config
        self.image = Image.new("RGB", (config.image_size, config.image_size), "black")
        self.font = ImageFont.truetype(config.font, 12)
        self.frames = list()

    def _create_image(self, base_img, vehicles):
        # simulate a sort of motion by taking previous image, dimming it 80% before
        # adding new positions
        img = ImageEnhance.Brightness(base_img).enhance(0.8)
        draw = ImageDraw.Draw(img)

        # fill in vehicle colours based on how delayed they are
        for vehicle in vehicles:
            splodge(draw, vehicle.x, vehicle.y, fill=vehicle.color())

        # draw the timestamp - requires us to paint a black rectangle to completely clear previous one
        timestamp_x = 10
        timestamp_y = self.config.image_size - 22
        draw.rectangle(
            [timestamp_x, timestamp_y, timestamp_x + 190, timestamp_y + 12],
            fill="black",
        )
        timestamp = datetime.now().isoformat()
        draw.text(
            (timestamp_x, timestamp_y),
            timestamp,
            font=self.font,
            fill=(255, 255, 255, 128),
        )

        return img

    def add_frame(self, vehicles):
        self.image = self._create_image(self.image, vehicles)
        self.frames.append(self.image.copy())

    def render(self):
        gif_filename = "./%s.gif" % datetime.now().isoformat().replace(":", ".")
        self.frames[0].save(
            gif_filename,
            save_all=True,
            append_images=self.frames[1:],
            duration=int(1000 * (1.0 / self.config.frames_per_second)),
            loop=0,
        )

        return gif_filename
