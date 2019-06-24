import pytest
from moto import mock_s3
import boto3


@pytest.fixture
@pytest.mark.filterwarnings('ignore::RuntimeWarning')
def s3_bucket():
    with mock_s3():
        boto3.client('s3').create_bucket(Bucket='lalala')
        yield boto3.resource('s3').Bucket('lalala')


class Test:
    def test_something(self, s3_bucket, tmpdir):
        s3_bucket.put_object(Key='anykey', Body='anybody')
        s3_bucket.download_file(Key='anykey', Filename=str(tmpdir / "tmp.txt"))
        assert (tmpdir / "tmp.txt").read() == "anybody"
