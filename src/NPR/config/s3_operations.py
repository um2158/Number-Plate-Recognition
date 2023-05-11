import os, sys, pickle
from src.NPR.logger import logging
from io import StringIO
from typing import List, Union
from src.NPR.config.aws_connection import S3Client
from mypy_boto3_s3.service_resource import Bucket
from src.NPR.exception import CustomException
from keras.models import load_model
from botocore.exceptions import ClientError
from pandas import DataFrame,read_csv

class S3Operation:
    def __init__(self):
        s3_client = S3Client()
        self.s3_resource = s3_client.s3_resource
        self.s3_client = s3_client.s3_client


    def get_bucket(self, bucket_name: str) -> Bucket:

            """
            Method Name :   get_bucket
            Description :   This method gets the bucket object based on the bucket_name
            
            Output      :   Bucket object is returned based on the bucket name
            """
            logging.info("Entered the get_bucket method of S3Operations class")
            try:
                bucket = self.s3_resource.Bucket(bucket_name)
                logging.info("Exited the get_bucket method of S3Operations class")
                return bucket
            
            except Exception as e:
                raise CustomException(e, sys) from e

    def download_file(self, bucket_name: str, output_file_path: str, key: str) -> None:

            """
            Method Name :   download_file
            Description :   This method downloads the file from the s3 bucket and saves the file in directory 
            
            Output      :   File is saved in local
            """
            logging.info("Entered the download_file method of S3Operation class")
            try:
                self.s3_resource.Bucket(bucket_name).download_file(key, output_file_path)
                logging.info("Exited the download_file method of S3Operation class")

            except Exception as e:
                raise CustomException(e, sys) from e

    def read_data_from_s3(self, bucket_filename: str, bucket_name: str, output_filepath: str) -> None:

            """
            Method Name :   read_data_from_s3
            Description :   This method downloads the file from the s3 bucket and saves the file in directory 
            
            Output      :   returns object.
            """
            logging.info("Entered the read_data_from_s3 method of S3Operation class")
            try:
                bucket = self.get_bucket(bucket_name)
                obj = bucket.download_file(Key=bucket_filename, Filename=output_filepath)
                logging.info("Exited the read_data_from_s3 method of S3Operation class")
                return obj
                
            except Exception as e:
                raise CustomException(e, sys) from e

    def upload_file(
        self,
        from_filename: str,
        to_filename: str,
        bucket_name: str,
        remove: bool = True,
    ) -> None:

        """
        Method Name :   upload_file
        Description :   This method uploads the from_filename file to bucket_name bucket with to_filename as bucket filename
        
        Output      :   Folder is created in s3 bucket
        """
        logging.info("Entered the upload_file method of S3Operations class")
        try:
            logging.info(
                f"Uploading {from_filename} file to {to_filename} file in {bucket_name} bucket"
            )

            self.s3_resource.meta.client.upload_file(
                from_filename, bucket_name, to_filename
            )
            logging.info(
                f"Uploaded {from_filename} file to {to_filename} file in {bucket_name} bucket"
            )

            if remove is True:
                os.remove(from_filename)
                logging.info(f"Remove is set to {remove}, deleted the file")
            else:
                logging.info(f"Remove is set to {remove}, not deleted the file")
            logging.info("Exited the upload_file method of S3Operations class")

        except Exception as e:
            raise CustomException(e, sys) from e

    def load_h5_model(self,bucket_name,object_file_name,local_file_name):
        try:
            self.download_file(bucket_name,local_file_name,object_file_name)

            model = load_model(local_file_name)

            return model
            
        except Exception as e:
            raise e 