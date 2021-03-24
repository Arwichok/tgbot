# Telegram structure bot | Alpha

## Init

### Create virtualenv

`make venv`

### Install packages

`make install`

or for dev

`make install_dev`

### Copy env and set your variables

`cp .env.dist .env`

## Start

`make start` 

## You can start bot as 
  1. Polling
  2. Webhook
  3. Web-Polling (Run Aiohttp App with polling)
  4. Gunicorn
