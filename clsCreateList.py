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
import numpy as np
from clsConfigClient import clsConfigClient as cf
import clsL as log
from pandas.util import hash_pandas_object

from datetime import datetime, timedelta

# Disbling Warning
def warn(*args, **kwargs):
    pass

import warnings
warnings.warn = warn

###############################################
###           Global Section                ###
###############################################

listCol = ['accessionYear', 'primaryImage', 'department', 'objectName', 'title',
'culture', 'period', 'artistDisplayName', 'artistNationality',
'artistBeginDate', 'artistEndDate', 'artistWikidata_URL', 'artistULAN_URL',
'objectDate', 'medium', 'dimensions', 'creditLine', 'country', 'objectURL',
'objectWikidata_URL', 'URL', 'AAT_URL', 'Wikidata_URL', 'elementName',
'elementDescription']

#Initiating Logging Instances
clog = log.clsL()

var = datetime.now().strftime(".%H.%M.%S")

documents = []

###############################################
###    End of Global Section                ###
###############################################
class clsCreateList:
    def __init__(self):
        self.basePath = cf.conf['DATA_PATH']
        self.fileName = cf.conf['FILE_NAME']
        self.Ind = cf.conf['DEBUG_IND']
        self.subdir = str(cf.conf['OUTPUT_DIR'])
        self.base_url = cf.conf['BASE_URL']
        self.outputPath = cf.conf['OUTPUT_PATH']
        self.mergedFile = cf.conf['MERGED_FILE']
        self.cleanedFile = cf.conf['CLEANED_FILE']

    def addDocument(self, content, source):
        new_doc = {
            "content": content,
            "meta": {"source": source}
        }
        documents.append(new_doc)

    def addHash(self, df):
        try:
            Ind = self.Ind
            subdir = self.subdir
            cleanedFile = self.cleanedFile

            df['artist_URL_hashed'] = hash_pandas_object(df['artist_URL'])
            df['object_URL_hashed'] = hash_pandas_object(df['object_URL'])
            df['Wiki_URL_hashed'] = hash_pandas_object(df['Wiki_URL'])
            df['Total_Hash'] = hash_pandas_object(df[['accessionYear', 'department', 'objectName', 'primaryImage', 'title', 'objectDate', 'country', 'artist_URL', 'object_URL', 'Wiki_URL']])

            # Save the filtered DataFrame to a new CSV file
            clog.logr(cleanedFile, Ind, df, subdir)

            return 0
        except Exception as e:
            x = str(e)
            print('Error: ', x)

            return 1

    def genPrompt(self, row):
        try:
            accessionYear = row['accessionYear']
            department = row['department']
            objectName = row['objectName']
            culture = row['culture']
            period = row['period']
            title = row['title']
            objectDate = row['objectDate']
            artistDisplayName = row['artistDisplayName']
            artistBeginDate = row['artistBeginDate']
            artistEndDate = row['artistEndDate']
            elementName = row['elementName']
            elementDescription = row['elementDescription']
            dimensions = row['dimensions']
            medium = row['medium']
            country = row['country']
            artistNationality = row['artistNationality']
            creditLine = row['creditLine']
            #artist_URL = row['artist_URL_hashed']
            #object_URL = row['object_URL_hashed']
            #primaryImage = row['primaryImage']
            #Wiki_URL = row['Wiki_URL_hashed']
            totalHash = row['Total_Hash']

            if (accessionYear is None):
                textPart_1 = "The Metropolitan Museum of Art's of"
            else:
                textPart_1 = "In " + str(accessionYear) + ", the Metropolitan Museum of Art's of"

            if (objectName is None):
                textPart_2 = "showcased an unknown masterpiece"
            else:
                textPart_2 = "showcased a masterpiece named the " + str(objectName)

            if (culture is None):
                textPart_3 = "from an unknown culture"
            else:
                textPart_3 = "from the " + str(culture)

            if (period is None):
                textPart_4 = " & from an unknown period"
            else:
                textPart_4 = "& of the " + str(period)

            if (objectDate is None):
                textPart_5 = "not established a proper timeline"
            else:
                textPart_5 = "Dated to approximately " + str(objectDate)

            if (artistDisplayName is None):
                textPart_6 = "and by an unknown creator"
            else:
                textPart_6 = "and crafted by " + str(artistDisplayName) + " between " + str(artistBeginDate) + " and " + str(artistEndDate) + " this work epitomizes " + str(artistNationality) + " craftsmanship"

            if (elementName is None):
                textPart_7 = ""
            else:
                textPart_7 = "this artifact is notable for its unique " + str(elementName) + '-' + str(elementDescription)

            if (dimensions is None):
                textPart_8 = ","
            else:
                textPart_8 = "with dimensions of " + str(dimensions).replace('\n', ' and ') + ","

            if (medium is None):
                textPart_9 = ""
            else:
                textPart_9 = "Produced from " + str(medium)

            if (country is None):
                textPart_10 = ", where origin of the country not established"
            else:
                textPart_10 = "and hailing from " + str(country)

            if (creditLine is None):
                textPart_11 = "with no clear credit-line"
            else:
                textPart_11 = "Its presence in the museum is highlighted by the " + str(creditLine)

            if (totalHash is None):
                textPart_12 = "Ref: {NO_DATA}"
            else:
                textPart_12 = "Ref: {'" + str(totalHash) + "'}"

            #if (artist_URL is None):
                #textPart_12 = "For an in-depth exploration of the artifact, one can read it from Wiki based on the avability."
            #else:
                #textPart_12 = "For an in-depth exploration of the artifact and its creator, visit the following Website: {" + str(artist_URL) + "}"

            #if (primaryImage is None):
                #textPart_13 = "."
            #else:
                #textPart_13 = ", and view its Image: {" + str(primaryImage) + "}"

            #if (Wiki_URL is None):
                #textPart_14 = "at this moment there is no authentic source or website available on this topic."
            #else:
                #textPart_14 = "with further information at - Wiki: {" + str(Wiki_URL) + "}"

            prompt = f"{textPart_1} {department} {textPart_2} {textPart_3} {textPart_4}, titled '{title}'. {textPart_5} {textPart_6}, {textPart_7} {textPart_8} {textPart_9} {textPart_10}. {textPart_11}. {textPart_12}"
            #prompt = f"{textPart_1} {department} {textPart_2} {textPart_3} {textPart_4}, titled '{title}'. {textPart_5} {textPart_6}, {textPart_7} {textPart_8} {textPart_9} {textPart_10}. {textPart_11}. {textPart_12} {textPart_13}. Additionally, the {title} is available in the public domain, {textPart_14}"

            return prompt

        except Exception as e:
            x = str(e)
            print('Error: ', x)

            return ''

    def createRec(self):
        try:
            basePath = self.basePath
            fileName = self.fileName
            Ind = self.Ind
            subdir = self.subdir
            base_url = self.base_url
            outputPath = self.outputPath
            mergedFile = self.mergedFile
            cleanedFile = self.cleanedFile

            FullFileName = outputPath + mergedFile

            df = pd.read_csv(FullFileName)
            df2 = df[listCol]
            dfFin = df2.drop_duplicates().reset_index(drop=True)

            dfFin['artist_URL'] = dfFin['artistWikidata_URL'].combine_first(dfFin['artistULAN_URL'])
            dfFin['object_URL'] = dfFin['objectURL'].combine_first(dfFin['objectWikidata_URL'])
            dfFin['Wiki_URL'] = dfFin['Wikidata_URL'].combine_first(dfFin['AAT_URL']).combine_first(dfFin['URL']).combine_first(dfFin['object_URL'])

            # Dropping the old Dtype Columns
            dfFin.drop(['artistWikidata_URL'], axis=1, inplace=True)
            dfFin.drop(['artistULAN_URL'], axis=1, inplace=True)
            dfFin.drop(['objectURL'], axis=1, inplace=True)
            dfFin.drop(['objectWikidata_URL'], axis=1, inplace=True)
            dfFin.drop(['AAT_URL'], axis=1, inplace=True)
            dfFin.drop(['Wikidata_URL'], axis=1, inplace=True)
            dfFin.drop(['URL'], axis=1, inplace=True)

            # Save the filtered DataFrame to a new CSV file
            #clog.logr(cleanedFile, Ind, dfFin, subdir)
            res = self.addHash(dfFin)

            if res == 0:
                print('Added Hash!')
            else:
                print('Failed to add hash!')

            # Generate the text for each row in the dataframe
            for _, row in dfFin.iterrows():
                x = self.genPrompt(row)
                self.addDocument(x, cleanedFile)

            return documents

        except Exception as e:
            x = str(e)
            print('Record Error: ', x)

            return documents
