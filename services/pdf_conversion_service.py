
import requests


class PDFConversionService:
    @staticmethod
    def convert_to_pdf(markdown: str) -> bytes:
        api_url = "https://markdowntopdf-production.up.railway.app/generate-pdf"
        headers = {"Content-Type": "application/json"}
        payload = {"markdown": markdown}

        response = requests.post(api_url, json=payload, headers=headers)

        if response.status_code != 200:
            return None

        return response.content
