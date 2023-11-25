from diagrams import Cluster, Diagram
from diagrams.custom import Custom
from diagrams.gcp.compute import AppEngine, KubernetesEngine
from diagrams.gcp.storage import Storage
from diagrams.onprem.client import User

with Diagram("Web Application Architecture", show=False):
    user = User("User")
    with Cluster("GCP Environment"):
        app_server = AppEngine("App Engine\nor\nKubernetes Engine")

        with Cluster("Services"):
            ocr_tool = Custom(
                "OCR (Google Cloud Vision API)",
                "./icons/google_vision_api_icon.png",
            )
            summarization_tool = Custom(
                "Text Summarization\n(OpenAI API)", "./icons/openai_icon.png"
            )
            database = Storage("Google Cloud Storage")

        notion_api = Custom("Notion API", "./icons/notion_icon.png")

    user >> app_server >> ocr_tool
    ocr_tool >> summarization_tool >> database
    database >> app_server >> notion_api
