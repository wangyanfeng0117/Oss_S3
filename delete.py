import math
import os
import json
import boto
import boto.s3.connection
from filechunkio import FileChunkIO

"""
账户名: wangyanfeng.vendor@tetras.ai, accessKey: H7H7L6BK4771XLKEN01E, secretKey: 6olSfac3c00sPcv2WXGPEBpnPYfQ8ArNLypmTPwR
账户名:  wangxin.vendor@tetras.ai, accessKey: ZL6BGO7S3EK18359BTSO, secretKey: gh1RI5dqAkXGNXHxDdAWwqAmkAN6BlqA8i6RB2TU
"""
AWS_S3_ENDPOINT_URL = 'oss-bj.sensetime.com'
AWS_ACCESS_KEY_ID = 'ZL6BGO7S3EK18359BTSO'
AWS_SECRET_ACCESS_KEY = 'gh1RI5dqAkXGNXHxDdAWwqAmkAN6BlqA8i6RB2TU'
BUCKET = 'ossr'


# 创建连接
def get_oss_connect():
    s3_conn = boto.connect_s3(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        host=AWS_S3_ENDPOINT_URL,
        port=80,
        is_secure=False,
        calling_format=boto.s3.connection.OrdinaryCallingFormat())
    return s3_conn


# 遍历当前bucket下的文件对象
def listobjects(conn, bucketname, prefix=''):
    """

    :param conn:
    :param bucketname: bucket桶名称
    :param prefix: 文件名称
    :return:
    """
    print('listobjects---------name=%s, prefix=%s' % (bucketname, prefix))
    bucket = conn.get_bucket(bucketname)
    obj = []
    for key in bucket.list(prefix):
        obj.append(key)
        print("{name}\t{size}\t{modified}\t{storageclass}".format(
            name=key.name,
            size=key.size,
            modified=key.last_modified,
            storageclass=key.storage_class,
        ))
    return obj

#删除当前ducket中的文件对象
def deleteobject(conn, bucketname, objname):
    print('deleteobject---- bucket=%s, object=%s' % (bucketname, objname))
    try:
        bucket = conn.get_bucket(bucketname)
        bucket.delete_key(objname)
    except Exception as e:
        print("deleteobject exception:", e)


if __name__ == '__main__':
    S3_conn = get_oss_connect()
    for obj in listobjects(S3_conn, BUCKET, 'c'):
        deleteobject(S3_conn, BUCKET, obj.name)

