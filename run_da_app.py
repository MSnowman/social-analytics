import os

from daapp.main import create_app

#app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app = create_app('dev')


if __name__ == '__main__':
    app.run(port=5002)
