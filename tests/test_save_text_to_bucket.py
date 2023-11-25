import pytest
from google.cloud import storage

from processing_img import save_text_to_bucket


class MockBlob:
    def __init__(self):
        self.upload_from_string_called = False

    def upload_from_string(self, _):
        self.upload_from_string_called = True


@pytest.fixture
def mock_storage_client(mocker):
    return mocker.patch("processing_img.storage.Client")


def test_save_text_to_bucket(mock_storage_client, mocker):
    # モックオブジェクトの設定
    mock_bucket = mocker.Mock()
    mock_blob = MockBlob()
    mock_storage_client().bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob

    # テスト対象の関数を呼び出す
    save_text_to_bucket("test_bucket", "test_file", "test_text")

    # 関数が期待通りに呼び出されたことを確認
    mock_storage_client().bucket.assert_called_once_with("test_bucket")
    mock_bucket.blob.assert_called_once_with("test_file")
    assert (
        mock_blob.upload_from_string_called
    ), "The method 'upload_from_string' was not called"


def test_save_text_to_bucket_raises_exception(mock_storage_client, mocker):
    # モックオブジェクトの設定
    mock_storage_client().bucket.side_effect = Exception("Error")

    # テスト対象の関数を呼び出すと例外が発生することを確認
    with pytest.raises(Exception) as e:
        save_text_to_bucket("test_bucket", "test_file", "test_text")
    assert str(e.value) == "Error"

    # 関数が期待通りに呼び出されたことを確認
    mock_storage_client().bucket.assert_called_once_with("test_bucket")


def test_save_text_to_bucket_with_empty_text(mock_storage_client, mocker):
    # モックオブジェクトの設定
    mock_bucket = mocker.Mock()
    mock_blob = MockBlob()
    mock_storage_client().bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob

    # テスト対象の関数を呼び出す
    save_text_to_bucket("test_bucket", "test_file", "")

    # 関数が期待通りに呼び出されたことを確認
    mock_storage_client().bucket.assert_called_once_with("test_bucket")
    mock_bucket.blob.assert_called_once_with("test_file")
    assert (
        mock_blob.upload_from_string_called
    ), "The method 'upload_from_string' was not called"
