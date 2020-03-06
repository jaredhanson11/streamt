'''
Api endpoints handling live streams.
'''
from flask import request
from flask_restful import Resource

from streamt_core.stream_management import StreamManager
from streamt_web import responses

from .. import db


class StreamStartController(Resource):
    '''API for publishing streams started.'''
    stream_manager: StreamManager = StreamManager(db.session)

    def post(self):
        '''
        Sets a stream as started, creates stream record.
        on_publish callback. Return 2xx to allow rtmp stream to be published.
        4xx to prevent stream from being opened/recorded.
        '''
        print(f'Posted start data: {str(request.form.to_dict())}')
        stream_key = request.form['name']
        new_stream = self.stream_manager.start_stream(stream_key)
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
        print(f'Posted stop data: {str(request.form.to_dict())}')
        stream_id = request.form['name']
        self.stream_manager.end_stream(stream_id)
        return responses.success('Stream ended.')
