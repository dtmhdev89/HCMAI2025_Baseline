from pydantic_settings import BaseSettings
from pydantic import Field
import os


# if USE_ENV_FILE:
#     from dotenv import load_dotenv

#     load_dotenv()



class MongoDBSettings(BaseSettings):
    MONGO_HOST: str = Field(..., alias='MONGO_HOST')
    MONGO_PORT: int = Field(..., alias='MONGO_PORT')
    MONGO_DB: str = Field(..., alias='MONGO_DB')
    MONGO_USER: str = Field(..., alias='MONGO_USER')
    MONGO_PASSWORD: str = Field(..., alias='MONGO_PASSWORD')


class IndexPathSettings(BaseSettings):
    FAISS_INDEX_PATH: str | None  
    USEARCH_INDEX_PATH: str | None

class KeyFrameIndexMilvusSetting(BaseSettings):
    COLLECTION_NAME: str = "keyframe"
    HOST: str = Field(..., alias="MILVUS_HOST")
    PORT: int = Field(..., alias="MILVUS_PORT")
    METRIC_TYPE: str = 'COSINE'
    INDEX_TYPE: str = 'FLAT'
    BATCH_SIZE: int =10000
    SEARCH_PARAMS: dict = {}
    
class AppSettings(BaseSettings):
    DATA_FOLDER: str  = "/media/tinhanhnguyen/Data3/Projects/HCMAI2025_Baseline/data/keyframe"
    ID2INDEX_PATH: str = "/media/tinhanhnguyen/Data3/Projects/HCMAI2025_Baseline/data/id2index.json"
    MODEL_NAME: str = "hf-hub:laion/CLIP-convnext_xxlarge-laion2B-s34B-b82K-augreg-soup"
    FRAME2OBJECT: str = '/media/tinhanhnguyen/Data3/Projects/HCMAI2025_Baseline/app/data/detections.json'
    ASR_PATH: str = '/media/tinhanhnguyen/Data3/Projects/HCMAI2025_Baseline/app/data/asr_proc.json'


