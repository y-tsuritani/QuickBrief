import pytest
from google.cloud import storage

from processing_img import process_images


@pytest.fixture
def mock_storage_blob(mocker):
    return mocker.patch("processing_img.storage.Blob")


@pytest.fixture
def mock_list_blobs_in_order(mocker):
    return mocker.patch("processing_img.list_blobs_in_order")


@pytest.fixture
def mock_extract_text_from_image(mocker):
    return mocker.patch("processing_img.extract_text_from_image")


@pytest.fixture
def mock_save_text_to_bucket(mocker):
    return mocker.patch("processing_img.save_text_to_bucket")


def test_process_images(
    mock_storage_blob,
    mock_list_blobs_in_order,
    mock_extract_text_from_image,
    mock_save_text_to_bucket,
    mocker,
):
    # モックオブジェクトの設定
    mock_list_blobs_in_order.return_value = ["file1", "file2"]
    mock_extract_text_from_image.return_value = "extracted text"

    # テスト対象の関数を呼び出す
    process_images("source_bucket", "destination_bucket")

    # 関数が期待通りに呼び出されたことを確認
    mock_list_blobs_in_order.assert_called_once_with("source_bucket")
    mock_storage_blob.assert_has_calls(
        [
            mocker.call(bucket=mocker.ANY, name="file1"),
            mocker.call(bucket=mocker.ANY, name="file2"),
        ]
    )
    mock_extract_text_from_image.assert_has_calls(
        [mocker.call(mocker.ANY), mocker.call(mocker.ANY)]
    )
    mock_save_text_to_bucket.assert_has_calls(
        [
            mocker.call("destination_bucket", "file1.txt", "extracted text"),
            mocker.call("destination_bucket", "file2.txt", "extracted text"),
        ]
    )
