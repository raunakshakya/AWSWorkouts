import logging
import boto3
from botocore.exceptions import ClientError
import datetime
import os

session = None
s3_client = None
NO_OF_BUCKETS_TO_CREATE = 2
FOLDER_WITH_OBJECTS = "files"


# Create an S3 bucket in a specified region
def create_bucket(bucket_name):
    region = session.region_name
    try:
        # Throws "InvalidLocationConstraint The specified location-constraint is not valid" if region is us-east-1
        # Reason: If a region is not specified, the bucket is created in the S3 default region (us-east-1)
        if region is None or region == "us-east-1":
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            location = {'LocationConstraint': region}  # LocationConstraint cannot be "us-east-1"
            s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    print(f"Created bucket {bucket_name}")
    return True


# Retrieve the list of existing buckets
def get_buckets():
    response = s3_client.list_buckets()
    return response['Buckets']


# Print the names of all the buckets
def print_buckets():
    buckets = get_buckets()
    if len(buckets) == 0:
        print("There are no buckets at this moment.")
    else:
        print('Existing buckets:')
        for bucket in buckets:
            print(f'  {bucket["Name"]}')


# Delete all the objects in the bucket
def empty_bucket(bucket_name):
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    if 'Contents' in response:
        for item in response['Contents']:
            object_key = item['Key']
            s3_client.delete_object(Bucket=bucket_name, Key=object_key)
            print(f"Deleted object {object_key} in bucket {bucket_name}")


if __name__ == "__main__":
    session = boto3.session.Session(profile_name="clioperation")
    # OR: Don't bother - keys are incorrect
    # session = boto3.session.Session(aws_access_key_id="AKIARV4MT4SSPGT6QH3",
    #                                 aws_secret_access_key="oB3Z3D2WLzYAabe/O+O2OhravXVT7kNrjrO2RNi",
    #                                 region_name="us-east-1")

    # print(session.region_name)  # us-east-1

    s3_client = session.client('s3')
    # Print existing buckets
    print_buckets()

    # Create NO_OF_BUCKETS_TO_CREATE number of buckets and upload all the files in FOLDER_WITH_OBJECTS
    for i in range(NO_OF_BUCKETS_TO_CREATE):
        ct = datetime.datetime.now()
        ts = round(ct.timestamp())
        bucket_name = "aws-demo-bucket-" + str(ts)
        create_bucket(bucket_name)

        files_to_upload = [f.name for f in os.scandir(FOLDER_WITH_OBJECTS) if f.is_file()]
        # print(files_to_upload)
        for object_name in files_to_upload:
            s3_client.upload_file(Filename=os.path.join(FOLDER_WITH_OBJECTS, object_name), Bucket=bucket_name,
                                  Key=object_name)
            print(f"Uploaded object {object_name} to bucket {bucket_name}")

    # Again print existing buckets
    print_buckets()

    # Empty all the existing buckets and delete them
    buckets = get_buckets()
    for bucket in buckets:
        bucket_name = bucket["Name"]
        empty_bucket(bucket_name)
        s3_client.delete_bucket(Bucket=bucket_name)
        print(f"Deleted bucket {bucket_name}")

    # Again print existing buckets
    print_buckets()
