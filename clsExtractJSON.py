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

import pandas as pd
import json
import requests
import os
from pandas import json_normalize
import numpy as np
import threading
from datetime import datetime, timedelta

from clsConfigClient import clsConfigClient as cf
import clsL as log

# Disbling Warning
def warn(*args, **kwargs):
    pass

import warnings
warnings.warn = warn

###############################################
###           Global Section                ###
###############################################

#Initiating Logging Instances
clog = log.clsL()

var = datetime.now().strftime(".%H.%M.%S")

image_columns_list = ['URL', 'objectID']
constituents_columns_list = ['constituentID', 'role', 'name', 'constituentULAN_URL', 'constituentWikidata_URL', 'gender', 'objectID']
tags_columns_list = ['term', 'AAT_URL', 'Wikidata_URL', 'objectID']
measurements_columns_list = ['elementName', 'elementDescription', 'elementMeasurements.Depth', 'elementMeasurements.Height', 'elementMeasurements.Width', 'objectID']
all_columns_list = ['objectID','isHighlight','accessionNumber','accessionYear','isPublicDomain','primaryImage','primaryImageSmall','department','objectName','title','culture','period','dynasty','reign','portfolio','artistRole','artistPrefix','artistDisplayName','artistDisplayBio','artistSuffix','artistAlphaSort','artistNationality','artistBeginDate','artistEndDate','artistGender','artistWikidata_URL','artistULAN_URL','objectDate','objectBeginDate','objectEndDate','medium','dimensions','creditLine','geographyType','city','state','county','country','region','subregion','locale','locus','excavation','river','classification','rightsAndReproduction','linkResource','metadataDate','repository','objectURL','objectWikidata_URL','isTimelineWork','GalleryNumber','URL','constituentID','role','name','constituentULAN_URL','constituentWikidata_URL','gender','term','AAT_URL','Wikidata_URL','elementName','elementDescription','elementMeasurements.Depth','elementMeasurements.Height','elementMeasurements.Width']

###############################################
###    End of Global Section                ###
###############################################

class clsExtractJSON:
    def __init__(self):
        self.basePath = cf.conf['DATA_PATH']
        self.fileName = cf.conf['FILE_NAME']
        self.Ind = cf.conf['DEBUG_IND']
        self.subdir = str(cf.conf['OUT_DIR'])
        self.base_url = cf.conf['BASE_URL']
        self.api_key = cf.conf['API_KEY']
        self.header_token = cf.conf['HEADER_TOKEN']
        self.outputPath = cf.conf['OUTPUT_PATH']
        self.mergedFile = cf.conf['MERGED_FILE']
        self.yearRange = cf.conf['YEAR_RANGE']

    def extract_additionalImages(self, data):
        try:
            df_all = pd.DataFrame(columns=image_columns_list)

            if 'additionalImages' in data and data['additionalImages']:
                df_temp = pd.DataFrame(data['additionalImages'], columns=['URL'])
                df_temp['objectID'] = data['objectID']

                # Check if any desired columns are missing and add them
                missing_cols = set(image_columns_list) - set(df_temp.columns)
                for col in missing_cols:
                    df_temp[col] = np.nan

                df = df_temp[image_columns_list]
            else:
                df = df_all

            return df
        except Exception as e:
            x = str(e)
            print('Error: ', x)

            df = pd.DataFrame(columns=image_columns_list)

            return df

    def extract_constituents(self, data):
        try:
            df_all = pd.DataFrame(columns=constituents_columns_list)

            if 'constituents' in data and data['constituents']:
                df_temp = json_normalize(data, record_path='constituents')
                df_temp['objectID'] = data['objectID']

                # Check if any desired columns are missing and add them
                missing_cols = set(constituents_columns_list) - set(df_temp.columns)
                for col in missing_cols:
                    df_temp[col] = np.nan

                df = df_temp[constituents_columns_list]
            else:
                df = df_all

            return df
        except Exception as e:
            x = str(e)
            print('Error: ', x)

            df = pd.DataFrame(columns=constituents_columns_list)

            return df

    def extract_tags(self, data):
        try:
            df_all = pd.DataFrame(columns=tags_columns_list)

            if 'tags' in data and data['tags']:
                df_temp = json_normalize(data, record_path='tags')
                df_temp['objectID'] = data['objectID']

                # Check if any desired columns are missing and add them
                missing_cols = set(tags_columns_list) - set(df_temp.columns)
                for col in missing_cols:
                    df_temp[col] = np.nan

                df = df_temp[tags_columns_list]
            else:
                df = df_all

            return df
        except Exception as e:
            x = str(e)
            print('Error: ', x)

            df = pd.DataFrame(columns=tags_columns_list)

            return df

    def extract_measurements(self, data):
        try:
            df_all = pd.DataFrame(columns=measurements_columns_list)

            if 'measurements' in data and data['measurements']:
                #df_temp = json_normalize(data, record_path='measurements', meta='objectID')
                df_temp = json_normalize(data, record_path='measurements')
                df_temp['objectID'] = data['objectID']

                # Check if any desired columns are missing and add them
                missing_cols = set(measurements_columns_list) - set(df_temp.columns)
                for col in missing_cols:
                    df_temp[col] = np.nan

                df = df_temp[measurements_columns_list]
            else:
                df = df_all

            return df
        except Exception as e:
            x = str(e)
            print('Error: ', x)

            df = pd.DataFrame(columns=measurements_columns_list)

            return df

    def createData(self, inputJson):
        try:
            var_1 = datetime.now().strftime("%H.%M.%S")
            data_str = inputJson
            subdir = self.subdir
            Ind = self.Ind

            # Assuming your JSON is stored in a string called data_str
            data = json.loads(data_str)

            # Main dataframe
            df_main = pd.json_normalize(data)
            df_main = df_main.drop(columns=['additionalImages', 'constituents', 'tags', 'measurements'], errors='ignore')

            # Nested attributes
            df_additionalImages = self.extract_additionalImages(data)
            df_constituents = self.extract_constituents(data)
            df_tags = self.extract_tags(data)
            df_measurements = self.extract_measurements(data)

            # Reset index for all DataFrames to ensure no index conflict:
            dataframes = [df_main, df_additionalImages, df_constituents, df_tags, df_measurements]
            for df in dataframes:
                df.reset_index(drop=True, inplace=True)

            # Merge main_df with each child DataFrame using a left join:
            merged_df = df_main.copy()

            child_dfs = [df_additionalImages, df_constituents, df_tags, df_measurements]
            for df in child_dfs:
                merged_df = merged_df.merge(df, on='objectID', how='left', right_index=False, left_index=False)

            #clog.logr('6.merged_df' + var_1 + '.csv', Ind, merged_df, subdir)

            return merged_df
        except Exception as e:
            x = str(e)
            print('Error: ', x)

            merged_df = pd.DataFrame(columns=all_columns_list)

            return merged_df


    def generateDateRange(self, start_date_str, end_date_str, gap_days=6):
        date_format = "%Y-%m-%d"
        start_date = datetime.strptime(start_date_str, date_format)
        end_date = datetime.strptime(end_date_str, date_format)

        date_ranges = []
        current_date = start_date
        while current_date <= end_date:
            date_ranges.append((current_date.strftime(date_format), (current_date + timedelta(days=gap_days)).strftime(date_format)))
            current_date += timedelta(days=gap_days + 1)  # +1 to avoid overlapping with the previous range

        return date_ranges

    def generateFirstDayOfLastTenYears(self):
        yearRange = self.yearRange
        date_format = "%Y-%m-%d"
        current_year = datetime.now().year

        date_ranges = []
        for year in range(current_year - yearRange, current_year + 1):
            first_day_of_year_full = datetime(year, 1, 1)
            first_day_of_year = first_day_of_year_full.strftime(date_format)
            date_ranges.append(first_day_of_year)

        return date_ranges

    def cleanDB(self, inputFileName, subdir):
        try:
            # Read the CSV file into a DataFrame
            var_1 = datetime.now().strftime("%H.%M.%S")
            Ind = self.Ind
            outputPath = self.outputPath

            FullFileName = outputPath + inputFileName

            print('Full Clean File Name:')
            print(str(FullFileName))

            df = pd.read_csv(FullFileName)

            filtered_df = df[df.iloc[:, 0].str.isnumeric().fillna(False)]

            # Save the filtered DataFrame to a new CSV file
            clog.logr('DF_' + var_1 + '.csv', Ind, filtered_df, subdir)

            return 0
        except Exception as e:
            x = str(e)
            print('Error: ', x)

            return 1

    def mergeCsvFilesInDirectory(self, directory_path, output_path, output_file):
        try:
            csv_files = [file for file in os.listdir(directory_path) if file.endswith('.csv')]
            data_frames = []

            for file in csv_files:
                encodings_to_try = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
                for encoding in encodings_to_try:
                    try:
                        FullFileName = directory_path + file
                        print('File Name: ', FullFileName)
                        df = pd.read_csv(FullFileName, encoding=encoding)
                        data_frames.append(df)
                        break  # Stop trying other encodings if the reading is successful
                    except UnicodeDecodeError:
                        continue

            if not data_frames:
                raise Exception("Unable to read CSV files. Check encoding or file format.")

            merged_df = pd.concat(data_frames, ignore_index=True)

            merged_full_name = os.path.join(output_path, output_file)
            merged_df.to_csv(merged_full_name, index=False)

            for file in csv_files:
                os.remove(os.path.join(directory_path, file))

            return 0

        except Exception as e:
            x = str(e)
            print('Error: ', x)
            return 1

    def getDataThread(self, dep, base_url, headers, payload, date_ranges, objVal, subdir, Ind):
        try:
            cnt = 0
            cnt_x = 1
            var_1 = datetime.now().strftime("%H.%M.%S")

            for x_start_date in date_ranges:
                try:
                    urlM = base_url + '/objects?metadataDate=' + str(x_start_date) + '&departmentIds=' + str(dep)

                    print('Nested URL:')
                    print(str(urlM))

                    response_obj = requests.request("GET", urlM, headers=headers, data=payload)
                    objectDets = json.loads(response_obj.text)

                    for obj_det in objectDets['objectIDs']:
                        objVal.append(obj_det)

                    for objId in objVal:
                        urlS = base_url + '/objects/' + str(objId)

                        print('Final URL:')
                        print(str(urlS))

                        response_det = requests.request("GET", urlS, headers=headers, data=payload)
                        objDetJSON = response_det.text

                        retDB = self.createData(objDetJSON)
                        retDB['departmentId'] = str(dep)

                        if cnt == 0:
                            df_M = retDB
                        else:
                            d_frames = [df_M, retDB]
                            df_M = pd.concat(d_frames)

                        if cnt == 1000:
                            cnt = 0
                            clog.logr('df_M_' + var_1 + '_' + str(cnt_x) + '_' + str(dep) +'.csv', Ind, df_M, subdir)
                            cnt_x += 1
                            df_M = pd.DataFrame()

                        cnt += 1

                except Exception as e:
                    x = str(e)
                    print('Error X:', x)
            return 0

        except Exception as e:
            x = str(e)
            print('Error: ', x)

            return 1

    def genData(self):
        try:
            base_url = self.base_url
            header_token = self.header_token
            basePath = self.basePath
            outputPath = self.outputPath
            mergedFile = self.mergedFile
            subdir = self.subdir
            Ind = self.Ind
            var_1 = datetime.now().strftime("%H.%M.%S")


            devVal = list()
            objVal = list()

            # Main Details
            headers = {'Cookie':header_token}
            payload={}

            url = base_url + '/departments'

            date_ranges = self.generateFirstDayOfLastTenYears()

            # Getting all the departments
            try:
                print('Department URL:')
                print(str(url))

                response = requests.request("GET", url, headers=headers, data=payload)
                parsed_data = json.loads(response.text)

                print('Department JSON:')
                print(str(parsed_data))

                # Extract the "departmentId" values into a Python list
                for dept_det in parsed_data['departments']:
                    for info in dept_det:
                        if info == 'departmentId':
                            devVal.append(dept_det[info])

            except Exception as e:
                x = str(e)
                print('Error: ', x)
                devVal = list()

            # List to hold thread objects
            threads = []

            # Calling the Data using threads
            for dep in devVal:
                t = threading.Thread(target=self.getDataThread, args=(dep, base_url, headers, payload, date_ranges, objVal, subdir, Ind,))
                threads.append(t)
                t.start()

            # Wait for all threads to complete
            for t in threads:
                t.join()

            res = self.mergeCsvFilesInDirectory(basePath, outputPath, mergedFile)

            if res == 0:
                print('Successful!')
            else:
                print('Failure!')

            return 0

        except Exception as e:
            x = str(e)
            print('Error: ', x)

            return 1
