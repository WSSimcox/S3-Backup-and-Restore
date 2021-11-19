# Created by William Simcox

import os
import sys

import boto3
from botocore.exceptions import ClientError

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')


# Function for downloading files from specified bucket into specified local path
def restore(bucket_name, bucket_directory, local_path):
    restored_count = 0
    bucket = s3.Bucket(bucket_name)
    for obj in bucket.objects.filter(Prefix=bucket_directory):
        new_path = local_path + "/" + obj.key
        # checking if directory exists
        if not os.path.exists(os.path.dirname(new_path)):
            os.makedirs(os.path.dirname(new_path))
        bucket.download_file(obj.key, new_path)
        print("File Restored: " + new_path)
        restored_count += 1
    if restored_count == 0:
        print("\nERROR: Failed to restore")
    else:
        print("\nTotal Files Restored: " + str(restored_count))


###################
# Start of program
###################
def main():
    if len(sys.argv) != 3:
        print("ERROR: Invalid number of arguments passed through.")
        sys.exit(0)

    target = sys.argv[1]
    local_path = sys.argv[2]

    # Splitting :: for bucket-name and directory-name
    split_target = target.split("::")
    bucket_name = str.lower(split_target[0])
    bucket_directory = split_target[1]

    # Removing trailing forward slash
    if local_path.endswith('\\'):
        local_path = str.lower(local_path[:-1])

    try:
        restore(bucket_name, bucket_directory, local_path)
    except ClientError:
        print("ERROR: Unable to restore - If there is whitespace in the names of your folders or files, surround your path in quotes.")


if __name__ == "__main__":
    main()
