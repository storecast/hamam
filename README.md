# [txtr](http://txtr.com/) API for web reading

This is the python wrapper for the [reaktor](http://txtr.com/reaktor/) rpc API.
It makes it easier to communicate with the reaktor for txtr web reading app.
It shares the user sessions with the django `txtr_skins` app.

## Configuration (development)

Copy `configs/dev.py.sample` into `configs/dev.py` and add the connection
string to the db, that is used by your django app:
```
SQLALCHEMY_DATABASE_URI = 'mysql://user:pass@localhost/txtr_skins'
```

## Run (development)

Make sure to install all the dependencies:
```
pip install -r requirements/dev.txt
```
To run the app:
```
cd hamam && python app.py
```

## Deployment
_Still to come._

## Expected behavior

One can find the specifications [here](https://jira.txtr.com/secure/attachment/68184/txtr_api.pdf).

## Running tests
_Still to come._
