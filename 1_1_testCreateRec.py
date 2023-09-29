#########################################################
#### Written By: SATYAKI DE                          ####
#### Written On: 27-Jun-2023                         ####
#### Modified On 28-Sep-2023                         ####
####                                                 ####
#### Objective: This is the main class that creates  ####
#### documents based on the historical data.         ####
####                                                 ####
#########################################################

from clsConfigClient import clsConfigClient as cf
import clsL as log
import clsCreateList as ccl

from datetime import datetime, timedelta

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
cl = ccl.clsCreateList()

var = datetime.now().strftime(".%H.%M.%S")

documents = []

###############################################
###    End of Global Section                ###
###############################################
def main():
    try:
        var = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        print('*'*120)
        print('Start Time: ' + str(var))
        print('*'*120)

        print('*'*240)
        print('Creating Index store:: ')
        print('*'*240)

        documents = cl.createRec()

        print('Inserted Sample Records: ')
        print(str(documents))
        print('\n')

        r1 = len(documents)

        if r1 > 0:
            print()
            print('Successfully Indexed sample records!')
        else:
            print()
            print('Failed to sample Indexed recrods!')

        print('*'*120)
        var1 = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        print('End Time: ' + str(var1))

    except Exception as e:
        x = str(e)
        print('Error: ', x)

if __name__ == '__main__':
    main()
