import pytest
from google.cloud import storage

from processing_img import list_blobs_in_order


class MockBlob:
    def __init__(self, name):
        self.name = name


@pytest.fixture
def mock_client(mocker):
    mock_client = mocker.Mock()
    mock_client.list_blobs.return_value = [MockBlob(f"file_{i}.txt") for i in range(5)]
    mocker.patch("processing_img.storage.Client", return_value=mock_client)
    return mock_client


def test_list_blobs_in_order(mock_client):
    bucket_name = "test-bucket"
    expected_files = [f"file_{i}.txt" for i in range(5)]
    assert list_blobs_in_order(bucket_name) == sorted(
        expected_files
    ), "The blob names should be returned in sorted order"


def test_list_blobs_in_order_raises_exception(mock_client, mocker):
    # モックオブジェクトの設定
    mock_client.list_blobs.side_effect = Exception("Error")

    # テスト対象の関数を呼び出すと例外が発生することを確認
    with pytest.raises(Exception) as e:
        list_blobs_in_order("test-bucket")
    assert str(e.value) == "Error"

    # 関数が期待通りに呼び出されたことを確認
    mock_client.list_blobs.assert_called_once_with("test-bucket")


def test_list_blobs_in_order_with_empty_bucket(mock_client):
    mock_client.list_blobs.return_value = []

    result = list_blobs_in_order("empty-bucket")

    assert result == [], "The result should be an empty list for an empty bucket"

    mock_client.list_blobs.assert_called_once_with("empty-bucket")
