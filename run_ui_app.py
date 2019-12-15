import os


from uiapp.main import create_app

app = create_app(os.getenv('BOILERPLATE_ENV') or 'loc')


if __name__ == '__main__':
    if app.config['ENV'] == 'local':
        app.run(port=5000)
    else:
        app.run(host="0.0.0.0", port=5000)