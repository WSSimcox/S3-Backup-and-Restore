# S3 Backup and Restore
**Arch and Design**

This application recursively traverses the files of a given absolute path to a local directory and 
backs up the said directory inside a specific bucket. This application can also restore from the 
cloud. In order to have created this Python app, AWS's Python SKD called "Boto3" allows this 
application to backup, update, and restore locally with a bucket.

  For backup.py, the user must input a bucket name, a bucket directory, and the absolute 
path to the local directory that the user wishes to backup. backup.py will add the valid local 
directory to the specified bucket inside of S3, and if there is no bucket present, the application 
will create one. Once the bucket is created, its directory name is searched for; if not present, it is 
also created. Once found or created, the local directory's absolute path is recursively searched 
using os.walk(). As the application walks through the directories, the files inside are uploaded to 
the bucket. If the file already exists, the local version's date modified is compared to the cloud's 
version. The file is updated if the local's modified date is greater/after the cloud's version. Once 
all directories are searched, the console will display how many files were created or updated.

  Restore.py is more straightforward; it takes in a bucket name, a bucket directory, and a 
local directory's absolute path where the files in the cloud will be restored/downloaded locally. 
First, the bucket's files are searched in the bucket's directory as the filter. Each directory and file's 
path is appended to the local path creating a new path. If this new path doesn't exist locally, then 
a new directory is created. The files are then restored/downloaded to the local directory. Once 
all files from the bucket have been restored, the console displays how many files were restored 
locally

**Please See "Description & Instructions.PDF" for further details**
