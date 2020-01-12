import os


from mlapp.main import create_app, Cor

app = create_app(os.getenv('BOILERPLATE_ENV') or 'loc')
Cor(app, resources=r'/api/*', allow_headers='Content-Type')


if __name__ == '__main__':
    if app.config['ENV'] == 'local':
        app.run(port=5001)
    else:
        app.run(host="0.0.0.0", port=5001)