from flask import Flask

from config.base import create_database_if_not_exists
from controllers.mission_controller import mission_blueprint
from controllers.target_controller import target_blueprint
from repository.database import create_tables


def create_app():
    app = Flask(__name__)

    app.register_blueprint(mission_blueprint, url_prefix='/api/mission')
    app.register_blueprint(target_blueprint, url_prefix='/api/target')

    return app


if __name__ == '__main__':
    create_database_if_not_exists()
    # drop_all_tables()
    create_tables()
    # setup_database_with_data()

    app = create_app()
    app.run(debug=True)
