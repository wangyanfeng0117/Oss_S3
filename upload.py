import math
import os
import json
import boto
import boto.s3.connection
from filechunkio import FileChunkIO

AWS_S3_ENDPOINT_URL = 'oss-bj.sensetime.com'
AWS_ACCESS_KEY_ID = 'H7H7L6BK4771XLKEN01E'
AWS_SECRET_ACCESS_KEY = '6olSfac3c00sPcv2WXGPEBpnPYfQ8ArNLypmTPwR'
BUCKET = 'ossr'


def get_oss_connect():
    s3_conn = boto.connect_s3(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        host=AWS_S3_ENDPOINT_URL,
        port=80,
        is_secure=False,
        calling_format=boto.s3.connection.OrdinaryCallingFormat())
    return s3_conn

# 在当前桶下分块上传文件
def upload_big_file_to_oss(file):
    """

    :param file: 文件路径
    :return: 上传成功返回代码
    """
    s3_conn = get_oss_connect()
    b = s3_conn.get_bucket(BUCKET)
    source_path = file
    source_size = os.stat(source_path).st_size
    mp = b.initiate_multipart_upload(os.path.basename(source_path), policy="public-read")

    chunk_size = 524288000
    chunk_count = int(math.ceil(source_size / float(chunk_size)))

    for i in range(chunk_count):
        offset = chunk_size * i
        bytes = min(chunk_size, source_size - offset)
        with FileChunkIO(source_path, 'r', offset=offset,
                         bytes=bytes) as fp:
            mp.upload_part_from_file(fp, part_num=i + 1, )

    result = mp.complete_upload()
    print(result)
    return result


# 在当前桶下新建桶分块上传文件
def upload_big_file_by_key(key, file):
    s3_conn = get_oss_connect()
    b = s3_conn.get_bucket(BUCKET)

    source_path = file
    source_size = os.stat(source_path).st_size
    mp = b.initiate_multipart_upload('sdk/' + key + '/' + os.path.basename(source_path), policy='public-read')

    chunk_size = 524288000
    chunk_count = int(math.ceil(source_size / float(chunk_size)))

    for i in range(chunk_count):
        offset = chunk_size * i
        bytes = min(chunk_size, source_size - offset)
        with FileChunkIO(source_path, 'r', offset=offset,
                         bytes=bytes) as fp:
            mp.upload_part_from_file(fp, part_num=i + 1, )

    result = mp.complete_upload()
    print(result)
    return result


if __name__ == '__main__':
    upload_big_file_to_oss('bucketpolicy.json')
    # upload_big_file_by_key('honor', 'upload_oss.py')
