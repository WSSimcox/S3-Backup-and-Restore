# Created by William Simcox

import os
import sys

import boto3
from botocore.exceptions import ClientError

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')
my_session = boto3.session.Session()
region_name = my_session.region_name


# This function will make a backup to the cloud of the
# specified directory to the specified “bucket”
def backup(directory_to_backup, bucket_name, bucket_directory):
    # Checking if bucket already exists
    bucket = s3.Bucket(bucket_name)
    try:
        s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': region_name})
        print("Backing up to new Bucket " + bucket_name)
    except ClientError:
        print("Backing up to existing Bucket " + bucket_name)

    # Splitting path to not include unnecessary directories before directory_to_backup
    split_path = directory_to_backup.split("\\")
    split_path = split_path[len(split_path) - 1]

    # variables for tracking upload and modify count
    files_created = 0
    files_modified = 0

    # Recursively going through directories to backup files
    for local_path, directories, files in os.walk(directory_to_backup):
        # Adding files with respect to their directories
        for file in files:
            local_path = local_path.replace("\\", "/")
            s3_path = local_path
            s3_path = bucket_directory + s3_path[s3_path.find(split_path):] + "/" + file
            try:
                if _check_if_exists(bucket, s3_path):
                    if _modified(bucket_name, local_path + "/" + file, s3_path):
                        s3_client.upload_file(local_path + "/" + file, bucket_name, s3_path)
                        files_modified += 1
                else:
                    s3_client.upload_file(local_path + "/" + file, bucket_name, s3_path)
                    files_created += 1
            except ClientError:
                continue

    print("\nFiles Backed up: " + str(files_created))
    print("Files Updated: " + str(files_modified))


# Function that checks if file already exists in the S3 bucket
def _check_if_exists(bucket, file) -> bool:
    objs = list(bucket.objects.filter(Prefix=file))
    if len(objs) > 0 and objs[0].key == file:
        return True
    else:
        print("Creating File: " + file)
        return False


# Function that checks if file has been modified
def _modified(bucket, local_file_path, s3_file_path) -> bool:
    local_file_modified_time = os.path.getmtime(local_file_path)
    remote_file_modified_time = s3.Object(bucket, s3_file_path).last_modified.timestamp()
    if local_file_modified_time > remote_file_modified_time:
        print("Updating File: " + s3_file_path)
        return True
    else:
        return False


###################
# Start of program
###################
def main():
    if len(sys.argv) != 3:
        print("ERROR: Invalid number of arguments passed through.")
        sys.exit(0)

    target = sys.argv[1]
    directory_to_backup = sys.argv[2]

    # Splitting :: for bucket-name and directory-name
    split_target = target.split("::")
    bucket_name = str.lower(split_target[0])
    bucket_directory = split_target[1] + "/"

    # Removing trailing forward slash
    if directory_to_backup.endswith('\\') or directory_to_backup.endswith('/'):
        directory_to_backup = str.lower(directory_to_backup[:-1])

    # Checking if valid directory
    if not os.path.isdir(directory_to_backup):
        print("ERROR: Invalid local directory " + directory_to_backup)
        sys.exit(0)

    directory_to_backup = directory_to_backup.replace("/", "\\")

    try:
        backup(directory_to_backup, bucket_name, bucket_directory)
    except ClientError:
        print("ERROR: Unable to backup - If there is whitespace in the names of your"
              " folders or files, surround your path in quotes. Also, don't have a"
              " trailing backslash if path is wrapped around quotes.")


if __name__ == "__main__":
    main()
