## Installation
* Be sure you have python3 installed
* Generate a token from Jenkins
* Retreive API keys from Datadog
* Either export the token and keys or add them to your `~/.bashrc`. Be sure to `source ~/.bashrc` after adding them.
```
export JENKINS_URL="https://<yourname>:<yourtoken>@roy.datad0g.com"
export DATADOG_API_KEY="<apikey>"
export DATADOG_APP_KEY="<apikey>"
```

* Clone this repo
```
$ cd scary-cat && pip3 isntall .
```

## Usage
```
Usage:
    scary-cat replace <host-id> [--override]
    scary-cat remove <host-id> [--many] [--override]
    scary-cat config
```
