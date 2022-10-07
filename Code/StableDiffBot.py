#!/usr/bin/env python3

# Imports for file access and system detection
import os  # interact with file system
import sys  # Needed to load settings file
import platform  # identify OS type

# Imports shared variables and settings
sys.path.insert(0, '../Settings')
import settings

# Standard Libraries
#import argparse
#from collections import Counter # use a Counter object
#import csv # read and write csv files
#import datetime # deal with datetime objects
#from functools import partial
#import io
import json
#import math # basic math functions
#import operator
#import random # randomization
#import re # regular expression support

# Tools for multiprocessing
#import multiprocessing
#import signal # smooth SIGINT handling (i.e., gracefully shut down on ^C)
#import time # timing
#import traceback # Error handling

# Store and load abstract python objects
#import pickle

#import numpy as np # Advanced C compiled math routines
#import scikitlearn as sk # algorithms and statistics
#import pandas as pd # statistics
#import statsmodels # regressions for pandas

# Web downloads
#import urllib2 # download files directly
#from selenium import webdriver # interact with webpages
#import tweepy # download from and interact with Twitter

# Terminal wizardry
#from subprocess import Popen, PIPE
#import curses

# Telegram bot components
import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler

# Stable diffusion components
import torch
from diffusers import StableDiffusionPipeline

# Interface support
#import Tkinter as tk

#Dealing with unicode text import from zip:
#zipin = zipfile.ZipFile('zip_file_address.zip')
#files = zipin.namelist()
#try:
#    text.append(io.StringIO(zipin.open(files[i]).read().decode('utf-8')).readlines())
#except UnicodeDecodeError:
#    text.append(io.StringIO(unicodedata.normalize('NFKD', zipin.open(files[i]).read().decode('cp1252'))).readlines())



logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Import tokens
# Set up the bot
with open(settings.TELEGRAM_KEYFILE, 'rt') as f:
    tokens = json.load(f)

# Import the model
pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4",
                                               revision="fp16",
                                               torch_dtype=torch.float16,
                                               use_auth_token=tokens['huggingface_token'])
pipe.to("cuda")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I send images from Stable Diffuser!  I will do this for each subsequent message you send.")


async def echo_sd(update: Update, context: ContextTypes.DEFAULT_TYPE, pipe=pipe):
    input_text = update.message.text
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Processing "' + input_text + '"')
    filename = ''.join(ch for ch in input_text if ch.isalnum())
    if len(filename) > 20:
        filename = filename[0:20]
    c = 0
    while os.path.exists("../Images/" + filename + str(c) + '.png'):
        c += 1
    with torch.autocast("cuda"):
        image = pipe(input_text, num_inference_steps=100)
    if image['nsfw_content_detected'][0]:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Prompt produced banned content, retrying with new random seed')
        with torch.autocast("cuda"):
            image = pipe(input_text, num_inference_steps=100)
    image = image['images'][0]
    
    image.save("../Images/" + filename + str(c) + '.png')
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open("../Images/" + filename + str(c) + '.png', 'rb'))


def worker():
    application = ApplicationBuilder().token(tokens['token']).build()

    # Handlers: identify input
    start_handler = CommandHandler('start', start)
    echo_sd_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo_sd)

    # Add functionality to the bot
    application.add_handler(start_handler)
    application.add_handler(echo_sd_handler)

    # run the bot
    application.run_polling()

    return True


if __name__ == '__main__':
    worker()

