from flask_script import Manager

from app import blueprint
from app.main import create_app, db

app = create_app()
app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)


@manager.command
def load():
    DATA_FILE_NAME = 'data/sample_user_data.jsonl'
    db.sync_db()
    # import json file
    db.import_from_source(DATA_FILE_NAME)

@manager.command
def run():
    app.run()


if __name__ == '__main__':
    manager.run()
    # manager.load()