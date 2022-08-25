#-- coding:utf8 --

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
AWS_ACCESS_KEY_ID = 'H7H7L6BK4771XLKEN01E'
AWS_SECRET_ACCESS_KEY = '6olSfac3c00sPcv2WXGPEBpnPYfQ8ArNLypmTPwR'
BUCKET = 'ossr'

"""
AWS_S3_ENDPOINT_URL : Endpoint网关地址
AWS_ACCESS_KEY_ID : 生成的密钥ID
AWS_SECRET_ACCESS_KEY ： 网页中生成的密钥
BUCKET ： 创建的BUCKET名称   命名规则：合法utf8字符，编码后字节长度不超过1024，不小于3. bucket名不能以'.'开头，不能包含0xff字符。
object命名规则：合法utf8字符，utf8编码后长度不能超过1024。
"""


#连接对象存储服务
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

    """
    :param conn: 传入生成的链接
    :param bucketname: 传入bucket的名称
    :return:
    """

    print('isBucketExist---------name=%s' % bucketname)
    isExist = conn.lookup(bucketname)
    if isExist is None:
        print('bucket=', bucketname, 'is not exist')
        conn.create_bucket(BUCKET)
        return False
    return True

#获取Policy
def getBucketPolicy(conn,bucketname):
    """

    :param conn:
    :param bucketname:
    :return:
    """
    bucket = conn.get_bucket(bucketname)
    policyjson = bucket.get_policy()
    print('get policy:', policyjson)

#设置PolicyJson
def setBucketPolicyJson(bucket):
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
    r = bucket.set_policy(bucketpolicy)
    print('set bucket policy response:', r)

#删除Policy
def deleteBucketPolicy(bucket):
    r = bucket.delete_policy()
    print('delete bucket policy, response:',r)

if __name__ == '__main__':
    s3_conn = get_oss_connect()
    b = s3_conn.get_bucket(BUCKET)
    setBucketPolicyJson(b)