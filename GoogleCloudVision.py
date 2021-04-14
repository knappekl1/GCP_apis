#Read text from pdf files into a string variable, save on local
from PyPDF2 import PdfFileReader, PdfFileWriter
import PySimpleGUI as pg
import os
import io
import subprocess
from google.cloud import vision 
from google.cloud import storage
import json
import re

#subs/functions
def upload_bytes(bucket_name, source_bytes, file_type, destination_blob_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_bytes = "bytes"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(source_bytes, content_type=file_type)

    print(
        "File {} uploaded to {}.".format(
            file_type, destination_blob_name
        )
    )

def async_detect_document(gcs_source_uri, gcs_destination_uri, file_type):
    """OCR with PDF/TIFF as source files on GCS"""

    # Supported mime_types are: 'application/pdf' and 'image/tiff'
    mime_type = file_type

    # How many pages should be grouped into each json output file.
    batch_size = 1

    client = vision.ImageAnnotatorClient()

    feature = vision.Feature(
        type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)

    gcs_source = vision.GcsSource(uri=gcs_source_uri)
    input_config = vision.InputConfig(
        gcs_source=gcs_source, mime_type=mime_type)

    gcs_destination = vision.GcsDestination(uri=gcs_destination_uri)
    output_config = vision.OutputConfig(
        gcs_destination=gcs_destination, batch_size=batch_size)

    async_request = vision.AsyncAnnotateFileRequest(
        features=[feature], input_config=input_config,
        output_config=output_config)

    operation = client.async_batch_annotate_files(
        requests=[async_request])

    print('Waiting for the operation to finish.')
    operation.result(timeout=420)

    # Once the request has completed and the output has been
    # written to GCS, we can list all the output files.
    storage_client = storage.Client()

    match = re.match(r'gs://([^/]+)/(.+)', gcs_destination_uri)
    bucket_name = match.group(1)
    prefix = match.group(2)

    bucket = storage_client.get_bucket(bucket_name)

    # List objects with the given prefix.
    blob_list = list(bucket.list_blobs(prefix=prefix))
    print('Output files:')
    for blob in blob_list:
        print(blob.name)

    # Process the first output file from GCS.
    # Since we specified batch_size=2, the first response contains
    # the first two pages of the input file.
    output = blob_list[0]

    json_string = output.download_as_string()
    response = json.loads(json_string)

    # # The actual response for the first page of the input file.
    first_page_response = response['responses'][0]
    annotation = first_page_response['fullTextAnnotation']
    return annotation

    # # Here we print the full text from the first page.
    # # The response contains more information:
    # # annotation/pages/blocks/paragraphs/words/symbols
    # # including confidence scores and bounding boxes
    # print('Full text:\n')
    # print(annotation['text'])


#Input filePath
pg.theme("Dark Blue 3")

layout = [
[pg.InputText(key="txtFile"), pg.FilesBrowse("Browse", file_types=(("PDF Files", "*.pdf"),))],
[pg.Checkbox("GCV enforce", key="GCV")],
[pg.Submit(), pg.Cancel()]
]

window = pg.Window("Select PDF file",layout)
event, values = window.read()
window.close()

if event == "Cancel" or event == None:
    exit()

filePath = values["txtFile"]
GcvForced = values["GCV"]

#create new txt file name for save in the same location
splitPath = os.path.split(filePath)
newFileName = splitPath[-1].replace(".pdf",".txt")
newFilePath = os.path.join(splitPath[0],newFileName)
#create the pdf file name and other data to save the split page in GCS
bucketName = "valuetools_newbucket1"
blobName = "temp.pdf"
doctype = "application/pdf"
source_uri = "gs://" + bucketName +"/" + blobName
destination_uri = "gs://" + bucketName +"/output.json"

#Get selected page
with open(filePath,"rb") as pdfObject:
    pdfReader = PdfFileReader(pdfObject)
    numPages = pdfReader.getNumPages()
    pageNum = pg.popup_get_text("Select any page of " + str(numPages))
    try:
        numPage = int(pageNum)-1
    except:
        pg.PopupError("Not a page number")
        exit()
    pdfPage = pdfReader.getPage(numPage)
    pdfText = pdfPage.extractText()

    #Save the extracted page to bytesIO
    pdfWriter = PdfFileWriter()
    pdfWriter.addPage(pdfPage)
    output_stream = io.BytesIO()

    #output_stream = open("temp.pdf","wb")
    pdfWriter.write(output_stream)
    output_stream.seek(0) # return to start of the stream(!important)
    
    #Save bytes to GCS
    upload_bytes(bucketName,output_stream.read(), doctype, blobName)
    output_stream.close()

#process files
if pdfText and not GcvForced: #save and show read in text
    with open (newFilePath, "w", encoding="utf-8") as writer:
        writer.write(pdfText)
    #open pdf
    #subprocess.Popen(splitPagePath,shell=True)
    #show extraxcted text
    pg.popup_scrolled(pdfText)
    exit()
else: #call GCV API
    pdfText = async_detect_document(source_uri, destination_uri,doctype)["text"]
    with open (newFilePath, "w", encoding="utf-8") as writer:
        writer.write(pdfText)
    #open pdf
    #subprocess.Popen(splitPagePath,shell=True)
    #show extraxcted text
    pg.popup_scrolled(pdfText)
    exit()
    
