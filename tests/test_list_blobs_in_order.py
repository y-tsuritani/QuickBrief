import sys
from pathlib import Path

import pytest
from google.cloud import storage

# このスクリプトのディレクトリの親ディレクトリを取得し、srcパスに追加
sys.path.append(str(Path(__file__).parent.parent / "src"))

from processing_img import list_blobs_in_order  # 関数が定義されているモジュール名に置き換えてください


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
