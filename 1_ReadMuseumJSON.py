#########################################################
#### Written By: SATYAKI DE                          ####
#### Written On: 27-Jun-2023                         ####
#### Modified On 28-Sep-2023                         ####
####                                                 ####
#### Objective: This is the main calling             ####
#### python script that will invoke the              ####
#### Musuem API & create the hsitorical data.        ####
####                                                 ####
#########################################################
import datetime
from clsConfigClient import clsConfigClient as cf

import clsExtractJSON as cej

########################################################
################    Global Area   ######################
########################################################

cJSON = cej.clsExtractJSON()

basePath = cf.conf['DATA_PATH']
outputPath = cf.conf['OUTPUT_PATH']
mergedFile = cf.conf['MERGED_FILE']

########################################################
################  End Of Global Area   #################
########################################################

# Disbling Warning
def warn(*args, **kwargs):
    pass

import warnings
warnings.warn = warn

def main():
    try:
        var = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        print('*'*120)
        print('Start Time: ' + str(var))
        print('*'*120)

        inputFileName = 'mergedFile.csv'
        subdir = 'output'

        r1 = cJSON.genData()
        #r1 = cJSON.mergeCsvFilesInDirectory(basePath, outputPath, mergedFile)
        #r1 = cJSON.cleanDB(inputFileName, subdir)

        if r1 == 0:
            print()
            print('Successfully Scrapped!')
        else:
            print()
            print('Failed to Scrappe!')

        print('*'*120)
        var1 = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        print('End Time: ' + str(var1))

    except Exception as e:
        x = str(e)
        print('Error: ', x)

if __name__ == '__main__':
    main()
