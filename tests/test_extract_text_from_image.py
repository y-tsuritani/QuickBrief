import sys
from pathlib import Path

import pytest
from google.cloud import storage, vision
from google.cloud.vision_v1 import types

# このスクリプトのディレクトリの親ディレクトリを取得し、srcパスに追加
sys.path.append(str(Path(__file__).parent.parent / "src"))

from processing_img import extract_text_from_image  # 関数が定義されているモジュール名に置き換えてください


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


def test_extract_text_from_image(mock_vision_client):
    # モックオブジェクトの設定
    mock_blob = MockBlob(content=b"test content")
    mock_response = Mock()
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
