from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
import io
from pypdf import PdfReader
import csv

app = FastAPI()


def extract_text_from_pdf(pdf_content):
    with io.BytesIO(pdf_content) as file:
        pdf_reader = PdfReader(file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
    return text


def convert_text_to_csv(text):
    # Assuming text is in a simple format, you might need more complex logic depending on your use case
    rows = [line.split() for line in text.split('\n')]
    csv_data = io.StringIO()
    csv_writer = csv.writer(csv_data)
    csv_writer.writerows(rows)
    return csv_data.getvalue()


@app.post("/convertpdf/")
async def create_upload_file(file: UploadFile = File(...)):
    # Check if the uploaded file is a PDF
    if file.filename.endswith(".pdf"):
        try:
            pdf_text = extract_text_from_pdf(await file.read())  # Read contents of the file
            csv_data = convert_text_to_csv(pdf_text)
            return StreamingResponse(io.StringIO(csv_data), media_type="text/csv",
                                     headers={"Content-Disposition": "attachment;filename=output.csv"})
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=400, detail="Uploaded file is not a PDF")
