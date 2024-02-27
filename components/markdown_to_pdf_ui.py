import streamlit as st
from io import BytesIO
from services.pdf_conversion_service import PDFConversionService


class MarkdownToPDFUI:
    @staticmethod
    def convert_to_pdf(markdown: str) -> BytesIO:
        pdf_content = PDFConversionService.convert_to_pdf(markdown)
        return BytesIO(pdf_content)

    @staticmethod
    def present(pdf_file):
        if pdf_file:
            st.download_button(
                label="Download PDF",
                data=pdf_file,
                file_name="document.pdf",
                mime="application/pdf",
                type="primary",
            )
        else:
            st.error("Failed to generate PDF")
