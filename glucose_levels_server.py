import json
import os

from flask import Flask, request
import sqlite3
import logging
from glucose_levels_web_app.utils import validate_request, execute_query

application = Flask(__name__)
con = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'db', 'glucose_levels.db'), check_same_thread=False)

_logger = logging.getLogger()


@application.route("/api/v1/levels/", methods=['GET'])
def get_levels_by_user_id():

    """
    Endpoint used to get glucose level data by user ID.
    :return: Glucose level data returned as a list of dictionaries.
    """

    _logger.info("Request received...")
    client_request = json.loads(request.get_data())
    _logger.info("Checking request is valid...")
    validate_request(client_request)
    _logger.info("Executing query...")
    query_result = execute_query(con, "SELECT timestamp, recording from levels where user_id=?", client_request['user_id'])
    # Converting to a list of dictionaries so that each field is easy to access nicely.
    _logger.info("Sending response")
    return json.dumps([{"timestamp": row[0], "glucose_level": row[1]} for row in query_result])


@application.route("/api/v1/levels/<id>", methods=['GET'])
def get_levels_by_recording_id(id):
    """
    :param id:
    :return:
    """

    print(id)
    return "hello"


if __name__ == '__main__':
    _logger.setLevel('INFO')
    application.run(debug=True)
