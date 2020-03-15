'''
Utils for common api response patterns.
'''
import logging

logger = logging.getLogger(__name__)

RESPONSE_HEADERS = {
    'Content-Type': 'application/json'
}


def success(json_success_response, status_code=200, extra_headers={}):
    '''
    Returns success json response.
    '''
    success_headers = {**RESPONSE_HEADERS, **extra_headers}
    return generic_response(
        json_success_response, status_code, success_headers)


def client_error(json_err_response, status_code=400, extra_headers={}):
    '''Returns client error json response.'''
    return error(json_err_response, status_code, extra_headers)


def server_error(json_err_response, status_code=500, extra_headers={}):
    '''Returns server error json response.'''
    return error(json_err_response, status_code, extra_headers)


def error(json_err_response, status_code, extra_headers={}):
    '''Returns error json response.'''
    error_headers = {**RESPONSE_HEADERS, **extra_headers}
    return generic_response(json_err_response, status_code, error_headers)


def generic_response(response: any, status_code: int, headers: dict):
    '''
    Returns generic response given the response, a status code, and set of
    headers
    '''
    logger.debug("Response:%s Status:%d Headers:%s",
                 str(response), status_code, str(headers))
    return response, status_code, headers
