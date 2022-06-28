from uuid import uuid4
import boto3
import os.path
from flask import current_app as app
from werkzeug.utils import secure_filename


def s3_upload(source_file, upload_dir, acl='public-read'):
    """ Uploads WTForm File Object to Amazon S3
        Expects following app.config attributes to be set:
            S3_KEY              :   S3 API Key
            S3_SECRET           :   S3 Secret Key
            S3_BUCKET           :   What bucket to upload to
            S3_UPLOAD_DIRECTORY :   Which S3 Directory.
        The default sets the access rights on the uploaded file to
        public-read.  It also generates a unique filename via
        the uuid4 function combined with the file extension from
        the source file.
    """
    destination_filename = secure_filename(source_file.data.filename)

    # Connect to S3 and upload file.
    session = boto3.session.Session(
        aws_access_key_id=app.config["S3_KEY"],
        aws_secret_access_key=app.config["S3_SECRET"],
        region_name=app.config["REGION"])
    s3 = session.resource("s3")
    b = s3.Bucket(app.config["S3_BUCKET"])
    key = "/".join([upload_dir, destination_filename])
    b.put_object(Body=source_file.data.read(), Key=key)

    return key

