'''
Provides heartbeat of an "alive" server.
'''
from time import time
from flask_restful import Resource

from .. import responses


class HeartbeatController(Resource):
    '''
    Controller with server's heartbeat.
    '''

    def get(self):
        '''
        Returns current time.
        '''
        ret = {'timenow': int(time())}
        return responses.success(ret, 200)
