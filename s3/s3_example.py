import boto
from moto import mock_s3
from s3.mymodule import MyModel


@mock_s3
def test_my_model_save():
    conn = boto.connect_s3()
    # We need to create the bucket since this is all in Moto's 'virtual' AWS account
    conn.create_bucket('mybucket')

    model_instance = MyModel('steve', 'is awesome')
    model_instance.save()

    assert conn.get_bucket('mybucket').get_key('steve')


# with context serves same purpose as decorator above
def test_my_model_save_2():
    with mock_s3():
        conn = boto.connect_s3()
        conn.create_bucket('mybucket')

        model_instance = MyModel('steve', 'is awesome')
        model_instance.save()

        assert conn.get_bucket('mybucket').get_key('steve').get_contents_as_string() == 'is awesome'


# stop and start mocking manually
def test_my_model_save_3():
    mock = mock_s3()
    mock.start()

    conn = boto.connect_s3()
    conn.create_bucket('mybucket')

    model_instance = MyModel('steve', 'is awesome')
    model_instance.save()

    assert conn.get_bucket('mybucket').get_key('steve').get_contents_as_string() == 'is awesome'

    mock.stop()
