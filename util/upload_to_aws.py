import os
import boto3
import botocore
from dotenv import load_dotenv

load_dotenv()


def upload_to_aws(filepath):
    # Step 1: Import the all necessary libraries and SDK commands.
    # file_content = open(filepath, "rb")
    # Step 2: The new session validates your request and directs it to your Space's specified endpoint using the AWS SDK.
    session = boto3.session.Session()
    client = session.client(
        "s3",
        endpoint_url="https://blr1.digitaloceanspaces.com",  # Find your endpoint in the control panel, under Settings. Prepend "https://".
        config=botocore.config.Config(
            s3={"addressing_style": "virtual"}
        ),  # Configures to use subdomain/virtual calling format.
        region_name="blr1",  # Use the region in your endpoint.
        aws_access_key_id="DO00AFG7AFYVWJKD3H3W",  # Access key pair. You can create access key pairs using the control panel or API.
        aws_secret_access_key="yWUlSuj26bkSuwZy8pn0dTf4/dokPhjjR6Gdd4EAye4",
    )  # Secret access key defined through an environment variable.

    # Step 3: Call the put_object command and specify the file to upload.

    client.upload_file(filepath, "retina-omr-storage", filepath)


# upload_to_aws("retina5.jpg", "retina5.jpg")
