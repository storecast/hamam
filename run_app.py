from os import path
import sys


def get_app():
    app_dir = path.join(path.dirname(path.abspath(__file__)), 'hamam')
    # `config.from_object` doesn't support relative imports
    sys.path.insert(0, app_dir)
    from hamam.app import app
    return app


application = get_app()

if __name__ == '__main__':
    application.run()
