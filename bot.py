from datetime import datetime
from video_tweet import VideoTweet
from vehicle import Vehicle
from gif_creator import GifCreator
from idsjmk_client import IdsJmkClient
from config import Config
import click


def send_tweet(filename):
    tweet = VideoTweet(filename)
    tweet.upload_init()
    tweet.upload_append()
    tweet.upload_finalize()
    timestamp = "{0:%Y}-{0:%m}-{0:%d} {0:%H}:{0:%M}".format(datetime.now())
    tweet.tweet("The last hour of DPMB traffic as at %s" % timestamp)


@click.command()
@click.option("--image-size", default=450, help="Width + height of generated GIF")
@click.option("--clip-length", default=10, help="Length of generated GIF (in seconds)")
@click.option("--fps", default=30, help="Frame rate of generated GIF")
@click.option(
    "--capture-delay",
    default=12,
    help="Time in seconds between each snapshot (i.e. 12 = we will produce a GIF frame every 12 seconds)",
)
@click.option("--once", default=False, help="Only produce a single capture")
def bot(image_size, clip_length, fps, capture_delay, once):
    """Create an animated GIF showing the positions of IDS JMK buses, trolleys and trams over time."""
    config = Config(
        image_size=image_size,
        clip_length=clip_length,
        frames_per_second=fps,
        time_between_captures=capture_delay,
        # hard-code the boundaries we want to set on the map - this is roughly
        # a bounding box of all the tram stations. buses go out quite far ...
        lat_max=49.246998,
        lat_min=49.13773,
        lng_max=16.692684,
        lng_min=16.507967,
        font="/usr/share/fonts/mononoki-Regular.ttf",
    )

    print("capturing rate: every %d seconds" % config.time_between_captures)
    print("frame rate: %d fps" % config.frames_per_second)
    print("clip length: %d seconds" % config.clip_length)

    while True:
        gif = GifCreator(config)
        client = IdsJmkClient(config)

        for vehicles in client.begin():
            output = "."
            try:
                gif.add_frame(vehicles)
            except:
                output = "!"
            print(output, end="", flush=True)

        gif_filename = gif.render()
        print(gif_filename)
        send_tweet(gif_filename)

        if once:
            break


if __name__ == "__main__":
    bot()
