#!/usr/bin/python3
"""
Starts AirBnB Flask main application run with command:
    $ HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd
    HBNB_MYSQL_HOST=127.0.0.1 HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db
    HBNB_MYSQL_HOST=127.0.0.1 HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

API_HOST = getenv('HBNB_API_HOST', '0.0.0.0')
API_PORT = getenv('HBNB_API_PORT', 5000)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_api(exception):
    """ Closes storage if we encounter an exception """
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """returns a status code response"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host=API_HOST, port=API_PORT, threaded=True)
