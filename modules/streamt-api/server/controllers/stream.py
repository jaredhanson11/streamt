'''
Api endpoints handling live streams.
'''
import logging

from flask import request, g
from flask_restful import Resource

from streamt_core.stream_management import StreamManager
from streamt_web import responses

from .. import jwt, db

logger = logging.getLogger(__name__)

stream_manager: StreamManager = StreamManager(db.session)


class StreamListController(Resource):
    '''/streams API resource'''

    @jwt.requires_auth
    def get(self):
        '''Get list of streams'''
        user_streams = stream_manager.get_user_streams(g.user)
        ret = {'streams': user_streams}
        return responses.success(ret)

    @jwt.requires_auth
    def post(self):
        '''Add a new stream'''
        pass


class StreamController(Resource):
    '''/streams/<id> API resource'''

    @jwt.requires_auth
    def get(self, id):
        pass

    @jwt.requires_auth
    def put(self, id):
        pass

    @jwt.requires_auth
    def delete(self, id):
        pass


class StreamStartController(Resource):
    '''API for publishing streams started.'''

    def post(self):
        '''
        Sets a stream as started, creates stream record.
        on_publish callback. Return 2xx to allow rtmp stream to be published.
        4xx to prevent stream from being opened/recorded.
        '''
        logger.debug('Posted start data: %s', str(request.form.to_dict()))
        stream_key = request.form['name']
        new_stream = stream_manager.start_stream(stream_key)
        if new_stream:
            redirect_headers = {
                'Location': f'rtmp://127.0.0.1/published/{new_stream.id}'}
            return responses.generic_response(None, 302, redirect_headers)
        else:
            return responses.client_error('Stream could not be started.')


class StreamStopController(Resource):
    '''
    API for publishing streams finished.
    This is in a different class than StreamStartController since both
    callbacks by nginx-rtmp-module are POST requests.
    '''

    def post(self):
        '''
        Sets a stream as finished.
        on_publish_done callback. Return code does not matter.
        '''
        logger.debug('Posted stop data: %s', str(request.form.to_dict()))
        stream_id = request.form['name']
        stream_manager.end_stream(stream_id)
        return responses.success('Stream ended.')
