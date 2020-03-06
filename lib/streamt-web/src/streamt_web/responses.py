'''
Utils for common api response patterns.
'''
import logging

logger = logging.getLogger(__name__)

RESPONSE_HEADERS = {
    'Content-Type': 'application/json'
}


def success(json_success_response, status_code=200):
    '''
    Returns success json response.
    '''
    success_headers = {}.update(RESPONSE_HEADERS)
    success_response = {'success': True, 'content': json_success_response}
    return generic_response(success_response, status_code, success_headers)


def client_error(json_err_response, status_code=400):
    '''Returns client error json response.'''
    return error(json_err_response, status_code)


def server_error(json_err_response, status_code=500):
    '''Returns server error json response.'''
    return error(json_err_response, status_code)


def error(json_err_response, status_code):
    '''Returns error json response.'''
    error_headers = {}.update(RESPONSE_HEADERS)
    error_response = {'success': False, 'content': json_err_response}
    return generic_response(error_response, status_code, error_headers)


def generic_response(response: any, status_code: int, headers: dict):
    '''
    Returns generic response given the response, a status code, and set of
    headers
    '''
    logger.debug("Response:%s Status:%d Headers:%s",
                 str(response), status_code, str(headers))
    return response, status_code, headers
