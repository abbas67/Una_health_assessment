import json
import os

from flask import Flask, request, abort, render_template
import sqlite3
import logging


from glucose_levels_web_app.utils import validate_request, execute_query

application = Flask(__name__)
application.config['MAX_CONTENT_LENGTH'] = None

con = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'db', 'glucose_levels.db'), check_same_thread=False)

_logger = logging.getLogger()


@application.route("/", methods=['GET'])
def index():
    """
    Home Page
    :return:
    """

    return render_template('index.html')


@application.route("/get_table_data", methods=['GET'])
def get_table_data():
    """
    Used to get table data to the frontend, usually this wouldn't be needed but in the interest of time...
    :return:
    """
    user_id = request.args['user_id']
    # Usually the frontend is a different server and would just make an api call to this server.
    query_result = execute_query(con, "SELECT * from levels where user_id=?", user_id)
    return render_template('index.html', table_data=list(query_result))


@application.route("/api/v1/levels/", methods=['GET'])
def get_levels_by_user_id():

    """
    API Endpoint used to get glucose level data by user ID.
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
    return json.dumps([{"timestamp": row[0], "glucose_level": row[1]} for row in list(query_result)])


@application.route("/api/v1/levels/<recording_id>", methods=['GET'])
def get_levels_by_recording_id(recording_id):
    """
    API for Getting glucose level readings by ID.
    :param recording_id: ID of glucose reading.
    :return:
    """

    _logger.info("Request received...")

    if not recording_id.isdigit():
        _logger.info("Malformed request, aborting...")
        abort(400)

    sql = "select * FROM levels WHERE recording_id=?"

    query_results = execute_query(con, sql, recording_id)

    if not query_results:
        _logger.info("ID not found, aborting...")
        abort(404)

    return json.dumps(query_results[0])


if __name__ == '__main__':
    _logger.setLevel('INFO')
    application.run()
