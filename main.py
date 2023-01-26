import logging
import sys
import os
import random
from pyrogram import Client, filters
from pytube import YouTube

log = logging.getLogger(__name__)


def logger_init():
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter(fmt="%(asctime)s - [%(levelname)s] - %(message)s",
                                  datefmt="%Y-%m-%d - %H:%M:%S")
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    log.addHandler(ch)


# todo: move to some json
bot_name = "YoutubeDownloaderBot"
api_id = 19977182
api_hash = "17090836bf8a86617ed5739248226128"

app = Client("my_account",
             api_id=api_id,
             api_hash=api_hash)


@app.on_message(filters.private & filters.command("start"))
async def start_handler(client, message):
    await message.reply(f"Welcome to {bot_name}!")


@app.on_message(filters.regex("(https?://)?(www\.)?\w+\.[a-z]+") & filters.private)
async def link_handler(client, message):
    #print(message)
    try:
        log.debug(f"trying")
        video_id = str(random.randint(100000, 999999))
        video_path = os.path.join(".", "video")

        yt = YouTube(message.web_page.url)
        log.info(f"url [{message.web_page.url}]")
        log.info(f"video_path [{video_path}]")
        log.info(f"video_id [{video_id}]")

        yt.streams.filter(progressive=True, file_extension='mp4')\
            .order_by('resolution')\
            .desc()\
            .first()\
            .download(output_path=video_path, filename=video_id)

        log.debug(f"sending {video_id}")

        await message.reply_video(os.path.join(video_path, video_id))

        log.debug(f"done, removing video [{video_id}]")

        os.remove(os.path.join(video_path, video_id))
        log.debug("workflow finished SUCCESS")

    except Exception as e:
        log.error(f"following exception caught\n{e}\n")
        log.debug(str(message))
        log.debug(f"sending error message to user")
        await message.reply("Not valid link or error")
        log.debug("workflow finished FAIL")


@app.on_message(filters.text & filters.private)
async def error_handler(client, message):
    #print(message)
    await message.reply("Waiting for link")


logger_init()
app.run()
