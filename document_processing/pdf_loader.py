
import io
import pymupdf
import pytesseract
from PIL import Image


def extract_pages_from_pdf(pdf_bytes, filename, use_ocr=True):
    """Extract text page-by-page from a PDF, using OCR as a fallback."""

    pages = []

    # Open PDF from uploaded bytes
    doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")

    for page_number, page in enumerate(doc, start=1):

        text = page.get_text("text").strip()

        # Use OCR if the extracted text is too short
        if use_ocr and len(text) < 30:
            try:
                pix = page.get_pixmap(
                    matrix=pymupdf.Matrix(2, 2),
                    alpha=False
                )

                image = Image.open(io.BytesIO(pix.tobytes("png")))

                ocr_text = pytesseract.image_to_string(image).strip()

                if ocr_text:
                    text = ocr_text

            except Exception as error:
                print(
                    f"OCR error in {filename}, "
                    f"page {page_number}: {error}"
                )

        if text:
            pages.append({
                "source": filename,
                "page": page_number,
                "text": text
            })

    doc.close()

    return pages
