from unittest import TestCase

import boto3


class TestBoto3(TestCase):
    def test_main(self):
        s3 = boto3.resource('s3')
        buckets = [bucket.name for bucket in s3.buckets.all()]
        print(buckets)

        for bucket in buckets:  # test-bucket-backend-bugsbunny
            if bucket == 'test-bucket-backend-bugsbunny':
                print('dio cane')
                return 1

        else:
            print('ahia')
            self.fail()
