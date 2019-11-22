import os

os.environ["BOILERPLATE_ENV"] = "prod"


from daapp.main import create_app

app = create_app(os.getenv('BOILERPLATE_ENV') or 'loc')


if __name__ == '__main__':
    app.run(port=5002)

