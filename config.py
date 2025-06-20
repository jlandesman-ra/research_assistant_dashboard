import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ASANA_ACCESS_TOKEN = os.getenv('ASANA_ACCESS_TOKEN', '2/1209642836801514/1210056798486740:cd38597d2fdb5a951348cbd4709855cb')
    PROJECT_GID = os.getenv('PROJECT_GID', '1209273054819416')
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here') 