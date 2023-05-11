import os,sys
from src.NPR.config.s3_operations import S3Operation
from src.NPR.entity.config_entity import *
from src.NPR.entity.artifacts_entity import *
from src.NPR.logger import logging
from src.NPR.exception import CustomException
from src.NPR.constants import *
from src.NPR.components.data_ingestion import DataIngestion
from src.NPR.components.data_transformation import DataTransformation
from src.NPR.components.prepare_base_model import PrepareBaseModel
from src.NPR.components.model_trainer import ModelTraining
from src.NPR.components.model_pusher import ModelPusher

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.prepare_base_model_config = PrepareBaseModelConfig()
        self.training_config = TrainingConfig()
        self.prepare_callbacks_config = PrepareCallbacksConfig()
        self.model_pusher_config = ModelPusherConfig()
        self.s3_operations = S3Operation()

    def start_data_ingestion(self)->DataIngestionArtifacts:
        logging.info("Entered the start_data_ingestion method of TrainPipeline class")
        try:
            logging.info("Getting the compressed data from S3 Bucket")
            data_ingestion_obj = DataIngestion(data_ingestion_config=self.data_ingestion_config,
            s3_operations=self.s3_operations)
            data_ingestion_artifact = data_ingestion_obj.initiate_data_ingestion()
            logging.info("Got the extracted data ")
            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e, sys)

    def start_data_transformation(self,data_ingestion_artifact : DataIngestionArtifacts)->DataTransformationArtifacts:
        try:
            logging.info("Entered the start_data_transformation method of TrainPipeline class")
            data_transformation_obj = DataTransformation(data_transformation_config=self.data_transformation_config,
            data_ingestion_artifact=data_ingestion_artifact)

            data_transformation_artifact = data_transformation_obj.initiate_data_transformation()
            logging.info("Exited the start_data_transformation method of TrainPipeline class")
            return data_transformation_artifact
            
        except Exception as e:
            raise CustomException(e, sys)

    def prepare_base_model(self)->PrepareBaseModelArtifacts:
        try:
            logging.info("Entered the prepare_callbacks method of TrainPipeline class")
            prepare_base_model_obj = PrepareBaseModel(prepare_base_model_config=self.prepare_base_model_config)
            prepare_base_model_artifact = prepare_base_model_obj.initiate_prepare_base_model()
            return prepare_base_model_artifact

        except Exception as e:
            raise CustomException(e, sys)

    def model_training(self,data_ingestion_artifact:DataIngestionArtifacts,
            data_transformation_artifact :DataTransformationArtifacts,
            prepare_base_model_artifact : PrepareBaseModelArtifacts
            ):
        try:
            logging.info("Entered the prepare_callbacks method of TrainPipeline class")
            training_obj = ModelTraining(
                training_config= self.training_config,
                prepare_callbacks_config= self.prepare_callbacks_config,
                data_ingestion_artifact= data_ingestion_artifact,
                data_transformation_artifact= data_transformation_artifact,
                prepare_base_model_artifact= prepare_base_model_artifact
            )
            model_trainer_artifact = training_obj.initiate_model_training()
            return model_trainer_artifact
            
        except Exception as e:
            raise CustomException(e, sys)

    def start_model_pusher(self,model_trainer_artifacts: ModelTrainerArtifacts, s3_operations: S3Operation):
        logging.info("Entered the start_model_pusher method of TrainPipeline class")
        try:
            model_pusher_obj = ModelPusher(model_pusher_config=self.model_pusher_config,
            model_trainer_artifacts= model_trainer_artifacts,
            s3_operations=s3_operations)

            model_pusher_obj.initiate_model_pusher()

        except Exception as e:
            raise CustomException(e, sys)
    
    def run_pipeline(self)->None:
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_transformation_artifact = self.start_data_transformation(data_ingestion_artifact)
            prepare_base_model_artifact = self.prepare_base_model()
            model_trainer_artifact = self.model_training(
                data_ingestion_artifact=data_ingestion_artifact,
                data_transformation_artifact = data_transformation_artifact,
                prepare_base_model_artifact=prepare_base_model_artifact)
            
            self.start_model_pusher(model_trainer_artifacts = model_trainer_artifact,s3_operations=self.s3_operations)
            
        except Exception as e:
            raise CustomException(e, sys)