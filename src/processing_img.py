import sys
from typing import List

from google.cloud import storage, vision
from google.cloud.vision_v1 import types


def list_blobs_in_order(bucket_name: str) -> List[str]:
    """
    指定されたバケット内のファイル名を昇順でリストアップします。

    Args:
        bucket_name (str): バケット名

    Returns:
        List[str]: ファイル名のリスト
    """
    storage_client = storage.Client()
    blobs = storage_client.list_blobs(bucket_name)
    return sorted(blob.name for blob in blobs)


def extract_text_from_image(image_blob: storage.Blob) -> str:
    """
    画像からテキストを抽出します。

    Args:
        image_blob (storage.Blob): Google Cloud StorageのBlobオブジェクト

    Returns:
        str: 抽出されたテキスト
    """
    client = vision.ImageAnnotatorClient()
    image = types.Image(content=image_blob.download_as_bytes())
    response = client.document_text_detection(image=image)
    return response.full_text_annotation.text


def save_text_to_bucket(bucket_name: str, file_name: str, text: str):
    """
    テキストを指定されたバケットに保存します。

    Args:
        bucket_name (str): バケット名
        file_name (str): ファイル名
        text (str): 保存するテキスト
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_string(text)


def process_images(source_bucket_name: str, destination_bucket_name: str):
    """
    画像を処理し、テキストを抽出して別のバケットに保存します。

    Args:
        source_bucket_name (str): ソースバケット名
        destination_bucket_name (str): 出力バケット名
    """
    file_names = list_blobs_in_order(source_bucket_name)
    for file_name in file_names:
        blob = storage.Blob(
            bucket=storage.Bucket(storage.Client(), source_bucket_name), name=file_name
        )
        text = extract_text_from_image(blob)
        save_text_to_bucket(destination_bucket_name, f"{file_name}.txt", text)


if __name__ == "__main__":
    source_bucket_name = sys.argv[1]
    destination_bucket_name = sys.argv[2]
    process_images(source_bucket_name, destination_bucket_name)
