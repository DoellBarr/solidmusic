<h2 align="center">Solid Music Bot</h2>
<p>
Telegram bot for stream music or video on telegram, 
powered by <a href="https://github.com/pytgcalls/pytgcalls">PyTgCalls</a>
and <a href="https://github.com/pyrogram/pyrogram">Pyrogram</a>
</p>

<div align="center">
    <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a> <br /> 
    <a href="https://github.com/pyrogram/pyrogram"><img src="https://img.shields.io/badge/Pyrogram-latest-blue?logo=github"></a>
    <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.10.4-blue?logo=python&logoColor=yellow"></a>
    <a href="https://github.com/pytgcalls/pytgcalls"><img src="https://img.shields.io/badge/PyTgCalls-0.9.0b1-blue?logo=github"></a> <br> <br>
    <a href="https://github.com/DoellBarr/solidmusic"><img src="https://img.shields.io/github/repo-size/doellbarr/solidmusic?logo=github"></a> <br>
    <a href="https://github.com/DoellBarr/solidmusic"><img src="https://img.shields.io/github/forks/DoellBarr/solidmusic?logo=github"></a>
    <a href="https://github.com/DoellBarr/solidmusic"><img src="https://img.shields.io/github/stars/DoellBarr/solidmusic?logo=github"></a>
</div>


<h3>Features</h3> 
<ul>
    <li>Playlist features</li>
    <li>Multi Language</li>
    <li>Maintained</li>
    <li>Less environment variables</li>
</ul>

<h3>Telegram</h3>
<ul>
    <a href="https://t.me/solidprojectsreborn"><img alt="SolidProject Channel" src="https://img.shields.io/badge/SolidProject-Channel-blue.svg?logo=telegram"></a> <br/>
    <a href="https://t.me/solidprojectsrebornchat"><img alt="SolidProject Support" src="https://img.shields.io/badge/SolidProject-Support-blue.svg?logo=telegram"></a> <br/>
</ul>

<h3>Deploy to Heroku </h3>
<div>
    <a href="https://www.heroku.com/deploy"><img src="https://www.herokucdn.com/deploy/button.svg"></a>
</div>

## IMPORTANT
### YOU NEED TO UPGRADE YOUR PYTHON VERSION TO 3.10* ON YOUR VPS
### IF YOU WANT TO USE THIS REPOSITORY

## Deploy to VPS
```bash
$ sudo su
apt-get update && apt-get upgrade -y
apt-get install curl
curl -sL https://deb.nodesource.com/setup_16.x | bash - 
apt-get install ffmpeg python3-pip python3-virtualenv nodejs -y 
git clone https://github.com/doellbarr/solidmusic && cd solidmusic 
virtualenv venv && . venv/bin/activate 
pip3 install --no-cache-dir -r requirements.txt 
cp sample.env .env 
nano .env  # fill it with your env 
python3 main.py
```