import os
from flask import Flask
from config import get_default_database_path


def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = os.environ.get(
        "SECRET_KEY", "dev-secret-key-change-in-production"
    )

    if test_config:
        app.config.update(test_config)
    else:
        app.config.setdefault("DATABASE", get_default_database_path())

    from models import init_app
    init_app(app)

    from auth import auth_bp
    app.register_blueprint(auth_bp)

    from blog import blog_bp
    app.register_blueprint(blog_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    #app.run(debug=True)
    # important, need to listent to all interfaces for docker container
    app.run(host='0.0.0.0')
