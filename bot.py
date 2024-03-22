# ========================ANZOR'S TELEGRAM BOT========================

from dotenv import load_dotenv
import os
import telebot
from pytube import YouTube

# Load environment variables from .env file
load_dotenv()

# Retrieve the BOT_TOKEN from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Initialize the bot
bot = telebot.TeleBot(BOT_TOKEN)


# ========================YOUTUBE DOWNLOADER========================
# 1) Download YouTube video function
def download_youtube_video(video_url, output_path):
    """
        Download a YouTube video.

        Parameters:
        - video_url (str): The URL of the YouTube video.
        - output_path (str): The path where the video will be saved.

        Returns:
        - str: Path to the downloaded video file if successful, None otherwise.


    yt = YouTube(video_url) - This line creates a YouTube object using the pytube library, passing the video_url as an argument.
    This object represents the YouTube video and allows us to interact with it programmatically.
    """
    try:
        yt = YouTube(video_url)
        stream = (
            yt.streams.get_highest_resolution()
        )  #  streams attribute of the YouTube object to get the highest resolution stream available for the video.
        video_file_path = os.path.join(
            output_path, yt.title + ".mp4"
        )  # Adding .mp4 and title to the output path
        stream.download(
            output_path
        )  # downloads the video stream and saves it to the specified output_path.
        return video_file_path
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# 2) Message handler for receiving YouTube video links
"""This is the condition for the message handler to be triggered. 
        It checks if the message's content type is "text" and if the text contains the substring "youtube.com/watch?v=". 
        If both conditions are true, the handler function (handle_youtube_link) will be invoked.
        """


@bot.message_handler(
    func=lambda message: message.content_type == "text"
    and ("youtube.com/watch?v=" in message.text or "youtu.be/" in message.text)
)
def handle_youtube_link(message):
    try:
        # Extract the YouTube video URL from the message
        video_url = message.text

        # Download the video
        output_path = "./downloads/"  # Set the output directory
        video_file_path = download_youtube_video(video_url, output_path)
        if video_file_path:
            # Send the downloaded video file to the user
            with open(video_file_path, "rb") as video_file:
                bot.send_video(message.chat.id, video_file)
            # Remove the downloaded file after sending
            os.remove(video_file_path)
        else:
            bot.reply_to(message, "Failed to download video.")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {e}")


# =================================ADDITIONAL MESSAGES HANDLER=========================
# Start command handler
# Sending the introductory message when the bot starts
@bot.channel_post_handler(func=lambda message: True)
def send_intro(message):
    if message.chat.type == "private" and message.text == "/start":
        intro_message = """Welcome to Anzor's Telegram Bot!
        I am here to help you download YouTube videos. 
        Just send me the link to the YouTube video you want to download, and I'll take care of the rest."""
        bot.reply_to(message, intro_message)


@bot.message_handler(commands=["strat", "hello", "Anzor"])
def send_welcome(message):
    bot.reply_to(
        message,
        "Hello, I am a bot built by Anzor. Please provide a valid YouTube video link and I will reply with downloaded video back to you.",
    )


@bot.message_handler(commands=["Артур"])
def echo_artur_message(message):
    bot.reply_to(message, "Рекстон Артур, ты кто такой? Давай, до свидания!")


@bot.message_handler(commands=["Леша"])
def echo_aдуч_message(message):
    bot.reply_to(
        message,
        "Лешкин картошкин! Когда уже пригласишь? Ответька пжлста! Только не тут это же бот как-никак!",
    )


# Echo handler
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, "Please provide a valid YouTube video link.")


# Start the bot
bot.infinity_polling()
