################################################
#### Written By: SATYAKI DE                 ####
#### Written On:  15-May-2020               ####
#### Modified On: 31-Aug-2023               ####
####                                        ####
#### Objective: This script is a config     ####
#### file, contains all the keys for        ####
#### personal OpenAI-based MAC-shortcuts    ####
#### enable bot.                            ####
####                                        ####
################################################

import os
import platform as pl

class clsConfigClient(object):
    Curr_Path = os.path.dirname(os.path.realpath(__file__))

    os_det = pl.system()
    if os_det == "Windows":
        sep = '\\'
    else:
        sep = '/'

    conf = {
        'APP_ID': 1,
        'ARCH_DIR': Curr_Path + sep + 'arch' + sep,
        'PROFILE_PATH': Curr_Path + sep + 'profile' + sep,
        'LOG_PATH': Curr_Path + sep + 'log' + sep,
        'DATA_PATH': Curr_Path + sep + 'data' + sep,
        'OUTPUT_PATH': Curr_Path + sep + 'output' + sep,
        'TEMP_PATH': Curr_Path + sep + 'temp' + sep,
        'IMAGE_PATH': Curr_Path + sep + 'Image' + sep,
        'SESSION_PATH': Curr_Path + sep + 'my-app' + sep + 'src' + sep + 'session' + sep,
        'OUTPUT_DIR': 'model',
        'APP_DESC_1': 'RAG Demo!',
        'DEBUG_IND': 'Y',
        'INIT_PATH': Curr_Path,
        'FILE_NAME': 'input.json',
        'MODEL_NAME': "gpt-3.5-turbo",
        'API_KEY': "4zHX5D5eKnHKdhfur87484jffjfjfDlvLP2eLHD7",
        'MODEL_NAME': 'gpt-3.5-turbo',
        'OPEN_AI_KEY': "sk-wVz5yI6kx4JYn3KDjf7rhfjfjf8jed4O6jrlxPKbv6Bgvv",
        'YOUTUBE_KEY': "AIzaSyDJdufruehdJJDFYKX8U-ElKiu2h-mvjd09sj",
        'BASE_URL': "https://collectionapi.metmuseum.org/public/collection/v1",
        'TITLE': "RAG Demo!",
        'TEMP_VAL': 0.2,
        'PATH' : Curr_Path,
        'MAX_TOKEN' : 400,
        'MAX_CNT' : 5,
        'OUT_DIR': 'data',
        'OUTPUT_DIR': 'output',
        'HEADER_TOKEN': 'JSESSIONID=B2784EKSIKS*&dkdjfdED33F0; __VCAP_ID__=0fa8c599-f9d4-4763-6795-bb25',
        'MERGED_FILE': 'mergedFile.csv',
        'CLEANED_FILE': 'cleanedFile.csv',
        'CLEANED_FILE_SHORT': 'cleanedFileMod.csv',
        'SUBDIR_OUT': 'output',
        'SESSION_CACHE_FILE': 'sessionCacheCounter.csv',
        'IMAGE_FILE': 'earth.jpeg',
        'CACHE_FILE': 'ragModelFaiss',
        'ADMIN_KEY': "Admin@23",
        'SECRET_KEY': "Adsec@23",
        "USER_NM": "Test",
        "USER_PWD": "Test@23",
        "VECTORDB_PATH": Curr_Path + sep + 'vectorDB' + sep,
        "VECTORDB_FILE_NM": "Q_A",
        "INPUT_VAL": 1000000000,
        "QUERY_MODEL": "facebook/dpr-question_encoder-single-nq-base",
        "PASSAGE_MODEL": "facebook/dpr-ctx_encoder-single-nq-base",
        'YEAR_RANGE': 1
    }
