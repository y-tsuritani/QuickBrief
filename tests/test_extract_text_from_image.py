import pytest
from google.cloud import storage, vision
from google.cloud.vision_v1 import types

from processing_img import extract_text_from_image


class MockBlob:
    def __init__(self, content):
        self.content = content

    def download_as_bytes(self):
        return self.content


@pytest.fixture
def mock_vision_client(mocker):
    mock_client = mocker.Mock()
    mocker.patch("processing_img.vision.ImageAnnotatorClient", return_value=mock_client)
    return mock_client


def test_extract_text_from_image(mock_vision_client, mocker):
    # モックオブジェクトの設定
    mock_blob = MockBlob(content=b"test content")
    mock_response = mocker.Mock()
    mock_response.full_text_annotation.text = "extracted text"
    mock_vision_client.document_text_detection.return_value = mock_response

    # テスト対象の関数を呼び出す
    result = extract_text_from_image(mock_blob)

    # 結果の確認
    assert result == "extracted text"

    # 関数が期待通りに呼び出されたことを確認
    mock_vision_client.document_text_detection.assert_called_once_with(
        image=types.Image(content=mock_blob.download_as_bytes())
    )


# OCRがテキストを検出できなかった場合のテスト
def test_extract_text_from_empty_image(mock_vision_client, mocker):
    mock_blob = MockBlob(content=b"")
    mock_response = mocker.Mock()
    mock_response.full_text_annotation.text = ""
    mock_vision_client.document_text_detection.return_value = mock_response

    result = extract_text_from_image(mock_blob)
    # 空のテキストを返す場合
    assert result == ""

    mock_vision_client.document_text_detection.assert_called_once_with(
        image=types.Image(content=mock_blob.download_as_bytes())
    )


# OCR処理中に例外が発生した場合のテスト
def test_extract_text_with_error(mock_vision_client, mocker):
    mock_blob = MockBlob(content=b"test content")
    mock_vision_client.document_text_detection.side_effect = Exception("Error")

    with pytest.raises(Exception) as e:
        extract_text_from_image(mock_blob)
    assert str(e.value) == "Error"

    mock_vision_client.document_text_detection.assert_called_once_with(
        image=types.Image(content=mock_blob.download_as_bytes())
    )


def test_extract_text_from_different_content_type(mock_vision_client, mocker):
    mock_blob = MockBlob(content=b"different content")
    mock_response = mocker.Mock()
    mock_response.full_text_annotation.text = "different extracted text"
    mock_vision_client.document_text_detection.return_value = mock_response

    result = extract_text_from_image(mock_blob)
    assert result == "different extracted text"

    mock_vision_client.document_text_detection.assert_called_once_with(
        image=types.Image(content=mock_blob.download_as_bytes())
    )
