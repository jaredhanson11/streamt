#!/usr/bin/env python3
'''
Find video files that have been finished. Upload video to S3. Delete uploaded
videos.

Required environment variables:

STREAMS_RECORD_PATH

S3_BUCKET
S3_REGION
S3_ENDPOINT

AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY

Optional environment variables:

S3_OBJECTS_PREFIX
'''
import logging
import re
import os
import sys
from datetime import datetime

import fcntl
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

S3_BUCKET_NAME = os.environ.get('S3_BUCKET')
STREAM_DIRECTORY = os.environ.get('STREAMS_RECORD_PATH')
S3_OBJECT_PREFIX = os.environ.get('S3_OBJECTS_PREFIX', "")
FILENAME_REGEX = re.compile('([0-9]*)-([0-9]*).flv')


def main():
    # Ensure environment variables are setup properly
    logger.info('Starting main method at UTC[%s]', str(datetime.utcnow()))
    _assert_env_setup()
    uploaded_files = upload_unlocked_files(STREAM_DIRECTORY)
    delete_uploaded_files(STREAM_DIRECTORY, uploaded_files)


def upload_unlocked_files(dirpath):
    '''
    Returns successfully uploaded files.
    '''
    uploaded_files = []

    # Get all unlocked video files and group them by stream_id
    streams_by_id = {}
    files_to_upload = sorted(get_unlocked_files(dirpath))
    for fname in files_to_upload:
        stream_id = FILENAME_REGEX.findall(fname)[0][0]
        if stream_id not in streams_by_id:
            streams_by_id[stream_id] = []
        streams_by_id[stream_id].append(fname)
    logger.debug('Stream files by id: %s', str(streams_by_id))

    # attempt to upload the files individually
    for stream_id, vid_fnames in streams_by_id.items():
        for fname in vid_fnames:
            object_name = f'{S3_OBJECT_PREFIX}{stream_id}/{fname}'
            logger.debug(
                'Attempting upload. object_name: %s, file_name: %s',
                object_name, fname)
            uploaded = _upload_file(os.path.join(
                dirpath, fname), S3_BUCKET_NAME, object_name)
            if uploaded:
                logger.debug(
                    'Successful upload. object_name: %s, file_name: %s',
                    object_name, fname)
                uploaded_files.append(fname)
    logger.debug('Files successfully uploaded: %s', str(uploaded_files))

    return uploaded_files


def get_unlocked_files(dirpath):
    '''
    Get all videos not currently being streamed written. Files that aren't
    finished being created (aka the stream is still recording this video file)
    are locked. Use fcntl to find videos that are finished being recorded aka
    ready to be uploaded to s3.
    '''
    filenames = os.listdir(dirpath)
    video_fnames = filter(_is_video_file, filenames)
    logger.debug('Stream videos: %s', str(list(video_fnames)))
    unlocked_fnames = list(filter(lambda fname: _is_file_unlocked(
        os.path.join(dirpath, fname)), video_fnames))
    logger.info('Unlocked videos: %s', str(unlocked_fnames))
    return unlocked_fnames


def delete_uploaded_files(dirpath, uploaded_fnames):
    '''Delete files that were succesfully uploaded'''
    for fname in uploaded_fnames:
        fpath = os.path.join(dirpath, fname)
        logger.debug('Deleting file: %s', fpath)
        os.remove(fpath)


# Helper functions
def _is_file_unlocked(filepath) -> bool:
    '''Return if file is unlocked or not'''
    try:
        fcntl.lockf(open(filepath, "a"), fcntl.LOCK_EX | fcntl.LOCK_NB)
        return True
    except IOError as ioerror:
        logger.debug('Locked file: %s', filepath)
        return False


def _is_video_file(filename) -> bool:
    '''Check if file is a video file'''
    return FILENAME_REGEX.match(filename) is not None


def _upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3',
                             region_name=os.environ.get('S3_REGION'),
                             endpoint_url=os.environ.get('S3_ENDPOINT'),
                             aws_access_key_id=os.environ.get(
                                 'AWS_ACCESS_KEY_ID'),
                             aws_secret_access_key=os.environ.get(
                                 'AWS_SECRET_ACCESS_KEY'))
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logger.warn(e)
        return False
    return True


def _assert_env_setup():
    '''Throw exception if missing required environment variables'''
    assert os.environ.get('S3_BUCKET') is not None
    assert os.environ.get('STREAMS_RECORD_PATH') is not None
    assert os.environ.get('S3_REGION') is not None
    assert os.environ.get('S3_ENDPOINT') is not None
    assert os.environ.get('AWS_ACCESS_KEY_ID') is not None
    assert os.environ.get('AWS_SECRET_ACCESS_KEY') is not None


if __name__ == '__main__':
    main()
