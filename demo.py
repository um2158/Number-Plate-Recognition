import sys
from src.NPR.exception import CustomException
from src.NPR.logger import logging
from src.NPR.pipeline.train_pipeline import TrainPipeline

train_obj = TrainPipeline()
train_obj.run_pipeline()