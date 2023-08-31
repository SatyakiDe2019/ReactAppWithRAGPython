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

from haystack.document_stores.faiss import FAISSDocumentStore
from haystack.nodes import DensePassageRetriever
import openai

from clsConfigClient import clsConfigClient as cf
import clsL as log

# Disbling Warning
def warn(*args, **kwargs):
    pass

import warnings
warnings.warn = warn

import os
import re
###############################################
###           Global Section                ###
###############################################
Ind = cf.conf['DEBUG_IND']
queryModel = cf.conf['QUERY_MODEL']
passageModel = cf.conf['PASSAGE_MODEL']

#Initiating Logging Instances
clog = log.clsL()

os.environ["TOKENIZERS_PARALLELISM"] = "false"

vectorDBFileName = cf.conf['VECTORDB_FILE_NM']

indexFile = "vectorDB/" + str(vectorDBFileName) + '.faiss'
indexConfig = "vectorDB/" + str(vectorDBFileName) + ".json"

print('File: ', str(indexFile))
print('Config: ', str(indexConfig))

# Also, provide `config_path` parameter if you set it when calling the `save()` method:
new_document_store = FAISSDocumentStore.load(index_path=indexFile, config_path=indexConfig)

# Initialize Retriever
retriever = DensePassageRetriever(document_store=new_document_store,
                                  query_embedding_model=queryModel,
                                  passage_embedding_model=passageModel,
                                  use_gpu=False)


###############################################
###    End of Global Section                ###
###############################################

class clsRAGOpenAI:
    def __init__(self):
        self.basePath = cf.conf['DATA_PATH']
        self.fileName = cf.conf['FILE_NAME']
        self.Ind = cf.conf['DEBUG_IND']
        self.subdir = str(cf.conf['OUT_DIR'])
        self.base_url = cf.conf['BASE_URL']
        self.outputPath = cf.conf['OUTPUT_PATH']
        self.vectorDBPath = cf.conf['VECTORDB_PATH']
        self.openAIKey = cf.conf['OPEN_AI_KEY']
        self.temp = cf.conf['TEMP_VAL']
        self.modelName = cf.conf['MODEL_NAME']
        self.maxToken = cf.conf['MAX_TOKEN']

    def extractHash(self, text):
        try:
            # Regular expression pattern to match 'Ref: {' followed by a number and then '}'
            pattern = r"Ref: \{'(\d+)'\}"
            match = re.search(pattern, text)

            if match:
                return match.group(1)
            else:
                return None
        except Exception as e:
            x = str(e)
            print('Error: ', x)

            return None

    def removeSentencesWithNaN(self, text):
        try:
            # Split text into sentences using regular expression
            sentences = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
            # Filter out sentences containing 'nan'
            filteredSentences = [sentence for sentence in sentences if 'nan' not in sentence]
            # Rejoin the sentences
            return ' '.join(filteredSentences)
        except Exception as e:
            x = str(e)
            print('Error: ', x)

            return ''

    def retrieveDocumentsReader(self, question, top_k=9):
        return retriever.retrieve(question, top_k=top_k)

    def generateAnswerWithGPT3(self, retrieved_docs, question):
        try:
            openai.api_key = self.openAIKey
            temp = self.temp
            modelName = self.modelName
            maxToken = self.maxToken

            documentsText = " ".join([doc.content for doc in retrieved_docs])

            filteredDocs = self.removeSentencesWithNaN(documentsText)
            hashValue = self.extractHash(filteredDocs)

            print('RAG Docs:: ')
            print(filteredDocs)
            #prompt = f"Given the following documents: {documentsText}, answer the question accurately based on the above data with the supplied http urls: {question}"

            # Set up a chat-style prompt with your data
            messages = [
                {"role": "system", "content": "You are a helpful assistant, answer the question accurately based on the above data with the supplied http urls. Only relevant content needs to publish. Please do not provide the facts or the texts that results crossing the max_token limits."},
                {"role": "user", "content": filteredDocs}
            ]

            # Chat style invoking the latest model
            response = openai.ChatCompletion.create(
                model=modelName,
                messages=messages,
                temperature = temp,
                max_tokens=maxToken
            )
            return hashValue, response.choices[0].message['content'].strip().replace('\n','\\n')
        except Exception as e:
            x = str(e)
            print('failed to get from OpenAI: ', x)
            return 'Not Available!'

    def ragAnswerWithHaystackAndGPT3(self, question):
        retrievedDocs = self.retrieveDocumentsReader(question)
        return self.generateAnswerWithGPT3(retrievedDocs, question)

    def getData(self, strVal):
        try:
            print('*'*120)
            print('Index Your Data for Retrieval:')
            print('*'*120)

            print('Response from New Docs: ')
            print()

            hashValue, answer = self.ragAnswerWithHaystackAndGPT3(strVal)

            print('GPT3 Answer::')
            print(answer)
            print('Hash Value:')
            print(str(hashValue))

            print('*'*240)
            print('End Of Use RAG to Generate Answers:')
            print('*'*240)

            return hashValue, answer
        except Exception as e:
            x = str(e)
            print('Error: ', x)
            answer = x
            hashValue = 1

            return hashValue, answer
