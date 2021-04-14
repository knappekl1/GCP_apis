from google.cloud import vision
from google.cloud import storage
import os
import io

def create_bucket(bucket_name):
    """Create a new bucket in specific location with storage class"""
    #bucket_name = "your-new-bucket-name"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    bucket.storage_class = "STANDARD"
    new_bucket = storage_client.create_bucket(bucket, location="europe-central2")

    print(
        "Created bucket {} in {} with storage class {}".format(
            new_bucket.name, new_bucket.location, new_bucket.storage_class
        )
    )
    return new_bucket

def delete_bucket(bucket_name):
    """Deletes a bucket. The bucket must be empty."""
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()

    bucket = storage_client.get_bucket(bucket_name)
    bucket.delete()

    print("Bucket {} deleted".format(bucket.name))


def upload_file(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

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

def download_file(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # source_blob_name = "storage-object-name"
    # destination_file_name = "local/path/to/file"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    # Construct a client side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
    # any content from Google Cloud Storage. As we don't need additional data,
    # using `Bucket.blob` is preferred here.
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print(
        "Blob {} downloaded to {}.".format(
            source_blob_name, destination_file_name
        )
    )

def download_bytes(bucket_name, source_blob_name):
    """Downloads a blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # source_blob_name = "storage-object-name"
    

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    # Construct a client side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
    # any content from Google Cloud Storage. As we don't need additional data,
    # using `Bucket.blob` is preferred here.
    blob = bucket.blob(source_blob_name)
    data = blob.download_as_string()
    

    print(
        "Blob {} downloaded.".format(
            source_blob_name
        )
    )

    return data

def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # blob_name = "your-object-name"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()

    print("Blob {} deleted.".format(blob_name))


#create_bucket("valuetools_newbucket1")
#delete_bucket("valuetools_newbucket1")

##upload from file
# filePath = "C:\\Users\\libor\\Dropbox\\python\\GoogleApis\\PDF_Scan_Sample.pdf"
# blobName = os.path.split(filePath)[-1]
# upload_file("valuetools_newbucket1",filePath, blobName)

##download to file
# bucketName = "valuetools_newbucket1"
# blobName = "PDF_Scan_Sample.pdf"
# savePath = "C:\\Users\\libor\\Dropbox\\python\\GoogleApis\\blob_downolad.pdf"
# download_file(bucketName, blobName, savePath)

##Delete file from Buckect
# bucketName = "valuetools_newbucket1"
# blobName = "PDF_Scan_Sample.pdf"
# delete_blob(bucketName, blobName)

##upload as bytes object
# bucketName = "valuetools_newbucket1"
# filePath = "C:\\Users\\libor\\Dropbox\\python\\GoogleApis\\PDF_Scan_Sample.pdf"
# blobName = os.path.split(filePath)[-1]
# docType = 'application/pdf'
# with open(filePath,"rb") as reader:
#     document = reader.read()
# upload_bytes(bucketName, document,docType,blobName)

##Dowload to memory
bucketName = "valuetools_newbucket1"
blobName = "PDF_Scan_Sample.pdf"
savePath = "C:\\Users\\libor\\Dropbox\\python\\GoogleApis\\blob_downolad_asbytes.pdf"

my_bytes = download_bytes(bucketName,blobName)

with open(savePath,"wb") as writer:
    writer.write(my_bytes)
