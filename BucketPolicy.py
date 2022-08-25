#-- coding:utf8 --

"""
账户名: wangyanfeng.vendor@tetras.ai, accessKey: H7H7L6BK4771XLKEN01E, secretKey: 6olSfac3c00sPcv2WXGPEBpnPYfQ8ArNLypmTPwR
账户名:  wangxin.vendor@tetras.ai, accessKey: ZL6BGO7S3EK18359BTSO, secretKey: gh1RI5dqAkXGNXHxDdAWwqAmkAN6BlqA8i6RB2TU
"""
import math, os
import json
import io
import boto
import boto.s3.connection
from boto.s3.lifecycle import Lifecycle, Transitions, Expiration, Rule
from filechunkio import FileChunkIO
from boto.s3.cors import CORSConfiguration

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

#判断Buckets是否存在
def isBucketExist(conn, bucketname):
    print('isBucketExist---------name=%s' % bucketname)
    isExist = conn.lookup(bucketname)
    if isExist is None:
        print('bucket=', bucketname, 'is not exist')
        conn.create_bucket('ossr')
        return False
    return True

#获取Policy
def getBucketPolicy(conn,bucketname):
    bucket = conn.get_bucket(bucketname)
    policyjson = bucket.get_policy()
    print('get policy:', policyjson)

#设置PolicyJson
def setBucketPolicyJson(b):
    bucket_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "AWS": [
                        "arn:aws:iam:::user/1d5e4735-b452-492c-8f8b-7d3e55a703a6"
                    ]
                },
                "Action": [
                    "s3:GetObject",
                    "s3:ListBucket"
                ],
                "Resource": [
                    "arn:aws:s3:::ossr",
                    "arn:aws:s3:::ossr/*"
                ]
            }
        ]
    }
    # Convert the policy from JSON dict to string
    bucketpolicy = json.dumps(bucket_policy)
    r = b.set_policy(bucketpolicy)
    print('set bucket policy response:', r)

#删除Policy
def deleteBucketPolicy(bucket):
    r = bucket.delete_policy()
    print('delete bucket policy, response:',r)

if __name__ == '__main__':
    s3_conn = get_oss_connect()
    b = s3_conn.get_bucket(BUCKET)
    setBucketPolicyJson(b)