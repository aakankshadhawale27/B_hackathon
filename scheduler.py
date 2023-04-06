import schedule
import time
import os
import boto3

dir_unstr = os.listdir("/mnt/d/cloudforge/files/unstructured/")
dir_str = os.listdir("/mnt/d/cloudforge/files/structured/")

print(dir_unstr)

def sendData(file,type):
    s3 = boto3.resource(
        's3',
        region_name='us-east-1',
        aws_access_key_id="AKIA454EGA5Z6J63DRFV",
        aws_secret_access_key="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"
    )

    try:
        if type == 1:
            os.chdir("D:/cloudforge/files/unstructured")
            content= open(file,"rb")
            s3.Object('unstructured-bucket',file).put(Body=content)
        elif type == 2:
            os.chdir("D:/cloudforge/files/structured")
            content= open(file,"rb")
            s3.Object('structured-bucket',file).put(Body=content)
            
    except:
        print("Please upload file again")
        

for file in dir_unstr:
    sendData(file,1)
    
for file in dir_str:
    sendData(file,2)
        



        



