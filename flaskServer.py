#########################################################
#### Written By: SATYAKI DE                          ####
#### Written On: 27-Jun-2023                         ####
#### Modified On 28-Jun-2023                         ####
####                                                 ####
#### Objective: This is the main calling             ####
#### python script that will invoke the              ####
#### shortcut application created inside MAC         ####
#### enviornment including MacBook, IPad or IPhone.  ####
####                                                 ####
#########################################################

from flask import Flask, jsonify, request, session
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import pandas as pd
from clsConfigClient import clsConfigClient as cf
import clsL as log
import clsContentScrapper as csc
import clsRAGOpenAI as crao
import csv
from datetime import timedelta
import os
import re
import json

########################################################
################    Global Area   ######################
########################################################
#Initiating Logging Instances
clog = log.clsL()

admin_key = cf.conf['ADMIN_KEY']
secret_key = cf.conf['SECRET_KEY']
session_path = cf.conf['SESSION_PATH']
sessionFile = cf.conf['SESSION_CACHE_FILE']

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes
app.config['JWT_SECRET_KEY'] = admin_key  # Change this!
app.secret_key = secret_key

jwt = JWTManager(app)

users = cf.conf['USER_NM']
passwd = cf.conf['USER_PWD']

cCScrapper = csc.clsContentScrapper()
cr = crao.clsRAGOpenAI()

# Disbling Warning
def warn(*args, **kwargs):
    pass

import warnings
warnings.warn = warn

# Define the aggregation functions
def join_unique(series):
    unique_vals = series.drop_duplicates().astype(str)
    return ', '.join(filter(lambda x: x != 'nan', unique_vals))

# Building the preaggregate cache
def groupImageWiki():
    try:
        base_path = cf.conf['OUTPUT_PATH']
        inputFile = cf.conf['CLEANED_FILE']
        outputFile = cf.conf['CLEANED_FILE_SHORT']
        subdir = cf.conf['SUBDIR_OUT']
        Ind = cf.conf['DEBUG_IND']

        inputCleanedFileLookUp = base_path + inputFile

        #Opening the file in dataframe
        df = pd.read_csv(inputCleanedFileLookUp)
        hash_values = df['Total_Hash'].unique()

        dFin = df[['primaryImage','Wiki_URL','Total_Hash']]

        # Ensure columns are strings and not NaN
        # Convert columns to string and replace 'nan' with an empty string
        dFin['primaryImage'] = dFin['primaryImage'].astype(str).replace('nan', '')
        dFin['Wiki_URL'] = dFin['Wiki_URL'].astype(str).replace('nan', '')

        dFin.drop_duplicates()

        #clog.logr(outputFile, Ind, dFin, subdir)

        # Group by 'Total_Hash' and aggregate
        dfAgg = dFin.groupby('Total_Hash').agg({'primaryImage': join_unique,'Wiki_URL': join_unique}).reset_index()

        #clog.logr('cleanedFileAgg.csv', Ind, dFin, subdir)

        return dfAgg

    except Exception as e:
        x = str(e)
        print('Error: ', x)

        df = pd.DataFrame()

        return df

resDf = groupImageWiki()

########################################################
################  End  Global Area  ####################
########################################################

def extractRemoveUrls(hash_value):
    image_urls = ''
    wiki_urls = ''
    # Parse the inner message JSON string
    try:

        print('Input Hash Value: ')
        print(str(hash_value))

        print('Sample ::')
        print(resDf.head(5))

        resDf['Total_Hash'] = resDf['Total_Hash'].astype(int)
        filtered_df = resDf[resDf['Total_Hash'] == int(hash_value)]

        print('filtered_df:')
        print(filtered_df.head(2))

        if not filtered_df.empty:
            image_urls = filtered_df['primaryImage'].values[0]
            wiki_urls = filtered_df['Wiki_URL'].values[0]

        print('Image_URLs:', str(image_urls))
        print('Wiki_URLs:', str(wiki_urls))

        return image_urls, wiki_urls

    except Exception as e:
        x = str(e)
        print('extractRemoveUrls Error: ', x)
        return image_urls, wiki_urls

def isIncomplete(line):
    """Check if a line appears to be incomplete."""

    # Check if the line ends with certain patterns indicating it might be incomplete.
    incomplete_patterns = [': [Link](', ': Approximately ', ': ']
    return any(line.endswith(pattern) for pattern in incomplete_patterns)

def filterData(data):
    """Return only the complete lines from the data."""

    lines = data.split('\n')
    complete_lines = [line for line in lines if not isIncomplete(line)]

    return '\n'.join(complete_lines)

def updateCounter(sessionFile):
    try:
        counter = 0

        # Check if the CSV file exists
        if os.path.exists(sessionFile):
            with open(sessionFile, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    # Assuming the counter is the first value in the CSV
                    counter = int(row[0])

        # Increment counter
        counter += 1

        # Write counter back to CSV
        with open(sessionFile, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([counter])

        return counter
    except Exception as e:
        x = str(e)
        print('Error: ', x)

        return 1

def getPreviousResult():
    try:
        fullFileName = session_path + sessionFile
        newCounterValue = updateCounter(fullFileName)

        return newCounterValue
    except Exception as e:
        x = str(e)
        print('Error: ', x)

        return 1

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    print('User Name: ', str(username))
    print('Password: ', str(password))

    #if username not in users or not check_password_hash(users.get(username), password):
    if ((username not in users) or (password not in passwd)):
        return jsonify({'login': False}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@app.route('/chat', methods=['POST'])
def get_chat():
    try:
        #session["key"] = "1D98KI"
        #session_id = session.sid
        #print('Session Id: ', str(session_id))

        cnt = getPreviousResult()
        print('Running Session Count: ', str(cnt))

        username = request.json.get('username', None)
        message = request.json.get('message', None)

        print('User: ', str(username))
        print('Content: ', str(message))

        if cnt == 1:
            retList = cCScrapper.extractCatalog()
        else:
            hashValue, cleanedData = cr.getData(str(message))
            print('Main Hash Value:', str(hashValue))

            imageUrls, wikiUrls = extractRemoveUrls(hashValue)
            print('Image URLs: ', str(imageUrls))
            print('Wiki URLs: ', str(wikiUrls))
            print('Clean Text:')
            print(str(cleanedData))
            retList = '{"records":[{"Id":"' + str(cleanedData) + '", "Image":"' + str(imageUrls) + '", "Wiki": "' + str(wikiUrls) + '"}]}'

        response = {
            'message': retList
        }

        print('JSON: ', str(response))
        return jsonify(response)

    except Exception as e:
        x = str(e)

        response = {
            'message': 'Error: ' + x
        }
        return jsonify(response)

@app.route('/api/data', methods=['GET'])
@jwt_required()
def get_data():
    response = {
        'message': 'Hello from Flask!'
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
