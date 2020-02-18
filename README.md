## Scary Cat
Replace your instances via host information on Datadog.

## Installation
* Be sure you have [python3](https://www.python.org/downloads/) installed. Check by using `python --version`.
* Go to your Jenkins Homepage -> Click on your name on the top right -> Configure -> Generate a API token.
* Retreive a API key and app key from Datadog. This is under Integrations -> APIs
* Either export the token and keys or add them to your `~/.bashrc`. Be sure to `source ~/.bashrc` after adding them. You may need to adjust your `JENKINS_URL` to the domain used for your Jenkins server.
```
export JENKINS_URL="https://<yourname>:<yourtoken>@jenkins/"
export DATADOG_API_KEY="<apikey>"
export DATADOG_APP_KEY="<apikey>"
```

* Clone this repo:
```
git clone https://github.com/ashley/scary-cat.git
```
* Start installing scary-cat as a CLI tool
```
cd scary-cat && pip3 isntall .
```

## Usage
```
Usage:
    scary-cat replace <host-id> [--override]
    scary-cat remove <host-id> [--many] [--override]
    scary-cat config
```

## Troubleshooting
* You may need to make sure [`Jinkies`](https://github.com/jmoiron/jinkies) was installed correctly. You can test this by just running `jinkies` in your terminal.
* If jobs are being executed but not showing up in your Jenkins service as a build in-progress, there may be an issue with your Jenkins URL.
