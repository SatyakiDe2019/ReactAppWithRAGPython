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

import clsFeedVectorDB as cfvd

from clsConfigClient import clsConfigClient as cf
import clsL as log

from datetime import datetime, timedelta

# Disbling Warning
def warn(*args, **kwargs):
    pass

import warnings
warnings.warn = warn

########################################################
################    Global Area   ######################
########################################################

cd = cfvd.clsFeedVectorDB()

########################################################
################  End Of Global Area   #################
########################################################

def main():
    try:
        var = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        print('*'*120)
        print('Start Time: ' + str(var))
        print('*'*120)

        print('*'*240)
        print('Creating vector-document store:: ')
        print('*'*240)

        #example_question = "What is the experience of 77th Street?"
        strVal = str(input("Your question here: "))
        r1 = cd.genData(strVal)

        if r1 == 0:
            print()
            print('Successfully Searched from RAG-OpenAI!')
        else:
            print()
            print('Failed to Search from RAG-OpenAI!')

        print('*'*120)
        var1 = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        print('End Time: ' + str(var1))

    except Exception as e:
        x = str(e)
        print('Error: ', x)

if __name__ == '__main__':
    main()
