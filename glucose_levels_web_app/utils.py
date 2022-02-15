import logging

from flask import abort

_logger = logging.getLogger()


def validate_request(client_input):
    """
    Basic Validation to make sure we don't bother processing anything improper.
    :param client_input: request data from the client.
    :return:
    """
    if not isinstance(client_input, dict):
        _logger.error("Incorrect request type, aborting...")
        abort(400)

    if 'user_id' not in client_input:
        _logger.error("malformed request, aborting...")
        abort(400)

    if not client_input['user_id']:
        _logger.error("malformed request, aborting...")
        abort(400)


def execute_query(con, sql, query_params):
    """
    Generic function used to execute sql queries and return results
    :param con: database connection.
    :param sql: sql string with tokens for params.
    :param query_params: params to be executed with sql.
    :return:
    """
    cur = con.cursor()
    cur.execute(sql, (query_params,))
    # So it is easier to work with in the future...
    return list(cur.fetchall())

