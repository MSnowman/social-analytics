import os


from flask_cors import CORS
from mlapp.main import create_app

app = create_app(os.getenv('BOILERPLATE_ENV') or 'loc')
CORS(app)

if __name__ == '__main__':
    if app.config['ENV'] == 'local':
        app.run(port=5001)
    else:
        app.run(host="0.0.0.0", port=5001)