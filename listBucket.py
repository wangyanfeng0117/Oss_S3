# -- coding:utf8 --

"""
账户名: wangyanfeng.vendor@tetras.ai, accessKey: H7H7L6BK4771XLKEN01E, secretKey: 6olSfac3c00sPcv2WXGPEBpnPYfQ8ArNLypmTPwR
账户名:  wangxin.vendor@tetras.ai, accessKey: ZL6BGO7S3EK18359BTSO, secretKey: gh1RI5dqAkXGNXHxDdAWwqAmkAN6BlqA8i6RB2TU
"""
import math
import os
import json
import io
import boto
import boto.s3.connection
from boto.s3.lifecycle import Lifecycle, Transitions, Expiration, Rule
from filechunkio import FileChunkIO
from boto.s3.cors import CORSConfiguration

AWS_S3_ENDPOINT_URL = 'oss-bj.sensetime.com'
AWS_ACCESS_KEY_ID = 'ZL6BGO7S3EK18359BTSO'
AWS_SECRET_ACCESS_KEY = 'gh1RI5dqAkXGNXHxDdAWwqAmkAN6BlqA8i6RB2TU'
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


def listobjects(conn, bucketname, prefix=''):
    print('listobjects---------name=%s, prefix=%s' % (bucketname, prefix))
    bucket = conn.get_bucket(bucketname)
    obj = []
    for key in bucket.list(prefix):
        obj.append(key)
    return obj


if __name__ == '__main__':
    S3_conn = get_oss_connect()
    for obj in listobjects(S3_conn, BUCKET, ''):
        print("{name}\t{size}\t{modified}\t{storageclass}".format(
            name=obj.name,
            size=obj.size,
            modified=obj.last_modified,
            storageclass=obj.storage_class,
        ))
