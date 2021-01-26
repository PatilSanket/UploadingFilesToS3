# -*- coding: utf-8 -*-
"""
Created on Wed Dec 30 21:15:41 2020

@author: Sanket
"""

import boto3
from flask import Flask, render_template, request
import pymongo

MongoDBAtlasURL = "Enter your connection URL here "
BucketName = "Enter your S3 bucket name"
DBName = "Name of database"
CollectionName = "Name of collection"

client = pymongo.MongoClient(MongoDBAtlasURL)

#Name of the database
mydb = client[DBName]

#Name of the collection
myCol = mydb[CollectionName]

s3Obj = boto3.client('s3',
                      region_name = 'ap-south-1',
                      aws_access_key_id = 'IAM User Access Key ID',
                      aws_secret_access_key = 'IAM User Secret Access Key')
    

app = Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def uploadFiles():
    if request.method =='GET':
        return render_template("index.html")
    if request.method == 'POST':
        obj = request.files['file']
        if obj:
                filename = obj.filename
                obj.save(filename)
                
                s3Obj.upload_file(
                    Bucket = BucketName,
                    Filename=filename,
                    Key = filename
                )
                
                url = "https://{}.s3.amazonaws.com/{}".format(BucketName,filename)
                mydict = { "FilePath": filename, "FileURL": url }
                x = myCol.insert_one(mydict)
                #print(x)
        
                msg = "The link to your hosted file: {0}. And the ObjID of inserted Document is: {1}".format(url,x) 
                print(msg)
                return render_template("index.html",msg = msg)

if __name__ == "__main__":
     app.run(debug=True)


