[![Build Status](https://travis-ci.org/txtr/hamam.svg?branch=master)](https://travis-ci.org/txtr/hamam)

# [txtr](http://txtr.com/) API for web reading

This is the python wrapper for the [reaktor](http://txtr.com/reaktor/) rpc API.
It makes it easier to communicate with the reaktor for txtr web reading app.
It shares the user sessions with the django `txtr_skins` app.

## Configuration (development)

Copy `hamam/configs/dev.py.sample` into `hamam/configs/dev.py` and add the connection
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
python run_app.py
```

## Deployment
_Still to come._

## Expected behavior

One can find the specifications [here](https://jira.txtr.com/secure/attachment/68184/txtr_api.pdf).

## Running tests

To test the whole application, run
```
python run_tests.py
```
If you want to test certain module(s), you can run
```
python run_tests.py mod_name another_mod_name
```

#### Adding new tests

If you want your module to be testable via `run_tests.py` script:

1. create your test cases and place them under `tests.py` file inside your module dir;
2. `tests.py` should have a `suite` function, that returns a test suite, based on your test cases. You can check an example in `session/tests.py`;
3. add your module name to `MODULE` variable in `run_tests.py`.


## Example setup with nginx and uwsgi

Here are 2 minimal configuration files to run the app on the path `/read/` using uwsgi (in http mode) and nginx.

First, the app need to run on its own using some ini file config for uwsgi:
```
[uwsgi]
chdir = /some/path/hamam/
home = /some/user/.virtualenvs/hamam/
master = True
processes = 1
pidfile = /some/path/hamam.pid
http = 127.0.0.1:8001
vacuum = True
env = HAMAM_SETTINGS=/some/path/hamam/hamam/configs.py
mount = /read=run_app.py
manage-script-name = True
```
The app is now available on port 8001, on both [http://127.0.0.1:8001/session/](http://127.0.0.1:8001/session/)
and [http://127.0.0.1:8001/read/session/](http://127.0.0.1:8001/read/session/).

Then, nginx just need to know about that path and on which port to forward traffic:
```
...

http {
	...

    server {
        listen 80;

        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
        }

        location /read/ {
            proxy_pass http://127.0.0.1:8001;
            proxy_set_header Host $host;
        }
    }
}
```
The app is now proxied from port 80: [http://127.0.0.1/read/session/](http://127.0.0.1/read/session/).
Any path different from `/read/` will be proxied to port 8000 and hits whatever is running there (e.g. a django app).
## License

BSD, see `LICENSE` for more details.

## Authors and contributors

txtr [Web team](mailto:web-dev@txtr.com).
