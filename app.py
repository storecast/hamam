from flask import Flask


app = Flask(__name__)
app.config.from_object('configs.default')
app.config.from_envvar('HAMAM_SETTINGS', silent=True)


if __name__ == '__main__':
    app.run()
