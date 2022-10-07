# StableDiffBot
Telegram bot to respond with Stable Diffusion images

## Installing dependencies

I personally use miniconda to manage my python backends.  As such, an environment.yml file is provided in this repository to help you set it up.  Do note that 1 package needs to be installed via pip though.

From the root of the directory, run:

```
conda env create -f environment.yml
conda activate SDBot
pip install python-telegram-bot --pre
```

If you prefer not to install via the `yml` file or want to change package versions, here is the full code used to set up the environment initially (note: mamba can be installed from conda as `conda install mamba`):

```
mamba create -n SDBot python=3.9 scipy ftfy
conda activate SDBot
mamba install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch
mambda install diffusers=0.3.0 transformers
conda install mkl-service
pip install python-telegram-bot --pre
```

## Software setup

First, you need to have a spare Telegram Bot.  If you don't have one, message the BotFather account on Telegram to set one up.  As part of the setup for the bot, you will be given a token for it; put this in the StableDiffBot.json file under `"token"`.

Second, you will need an account at HuggingFace: https://huggingface.co/ . Make an account there, and then you will get a token from them.  Put this token in StableDiffBot.json under `"huggingface_token"`.

Lastly, you need to accept the license agreement terms for Stable Diffusion v1.4 at https://huggingface.co/CompVis/stable-diffusion-v1-4 .  Just check the box and accept the terms and you are ready to go!

## Hardware used

My bot is running on a Ubuntu server with a GTX 1080.  At a minimum, you need ~4GB VRAM in an Nvidia GPU to use the code in this repository.

If you have a GPU with 10GB of VRAM, consider removing the lines `revision="fp16",` and `torch_dtype=torch.float16,` in order to use the full version of the model.

If you don't have a GPU, you'll need to remove the line `pipe.to("cuda")` and change both mentions of `torch.autocast("cuda")` to `torch.autocast("cpu")`.  Note that this runs significantly slower on even a high-end, modern CPU.