#########################################################
#### Written By: SATYAKI DE                          ####
#### Written On: 27-Jun-2023                         ####
#### Modified On 28-Sep-2023                         ####
####                                                 ####
#### Objective: This is the main calling             ####
#### python script that will invoke the              ####
#### haystack frameowrk to contextulioze the docs    ####
#### inside the vector DB.                           ####
####                                                 ####
#########################################################

from haystack.document_stores.faiss import FAISSDocumentStore
from haystack.nodes import DensePassageRetriever
import openai
import pandas as pd
import os
import clsCreateList as ccl

from clsConfigClient import clsConfigClient as cf
import clsL as log

from datetime import datetime, timedelta

# Disbling Warning
def warn(*args, **kwargs):
    pass

import warnings
warnings.warn = warn

###############################################
###           Global Section                ###
###############################################

Ind = cf.conf['DEBUG_IND']
openAIKey = cf.conf['OPEN_AI_KEY']

os.environ["TOKENIZERS_PARALLELISM"] = "false"

#Initiating Logging Instances
clog = log.clsL()
cl = ccl.clsCreateList()

var = datetime.now().strftime(".%H.%M.%S")

# Encode your data to create embeddings
documents = []

var_1 = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
print('*'*120)
print('Start Time: ' + str(var_1))
print('*'*120)

print('*'*240)
print('Creating Index store:: ')
print('*'*240)

documents = cl.createRec()

print('Inserted Sample Records: ')
print(documents[:5])
print('\n')
print('Type:')
print(type(documents))

r1 = len(documents)

if r1 > 0:
    print()
    print('Successfully Indexed records!')
else:
    print()
    print('Failed to Indexed recrods!')

print('*'*120)
var_2 = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
print('End Time: ' + str(var_2))

# Passing OpenAI API Key
openai.api_key = openAIKey

###############################################
###    End of Global Section                ###
###############################################

class clsFeedVectorDB:
    def __init__(self):
        self.basePath = cf.conf['DATA_PATH']
        self.modelFileName = cf.conf['CACHE_FILE']
        self.vectorDBPath = cf.conf['VECTORDB_PATH']
        self.vectorDBFileName = cf.conf['VECTORDB_FILE_NM']
        self.queryModel = cf.conf['QUERY_MODEL']
        self.passageModel = cf.conf['PASSAGE_MODEL']

    def retrieveDocuments(self, question, retriever, top_k=3):
        return retriever.retrieve(question, top_k=top_k)

    def generateAnswerWithGPT3(self, retrievedDocs, question):
        documents_text = " ".join([doc.content for doc in retrievedDocs])
        prompt = f"Given the following documents: {documents_text}, answer the question: {question}"

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()

    def ragAnswerWithHaystackAndGPT3(self, question, retriever):
        retrievedDocs = self.retrieveDocuments(question, retriever)
        return self.generateAnswerWithGPT3(retrievedDocs, question)

    def genData(self, strVal):
        try:
            basePath = self.basePath
            modelFileName = self.modelFileName
            vectorDBPath = self.vectorDBPath
            vectorDBFileName = self.vectorDBFileName
            queryModel = self.queryModel
            passageModel = self.passageModel

            print('*'*120)
            print('Index Your Data for Retrieval:')
            print('*'*120)

            FullFileName = basePath + modelFileName
            FullVectorDBname = vectorDBPath + vectorDBFileName

            sqlite_path = "sqlite:///" + FullVectorDBname + '.db'
            print('Vector DB Path: ', str(sqlite_path))

            indexFile = "vectorDB/" + str(vectorDBFileName) + '.faiss'
            indexConfig = "vectorDB/" + str(vectorDBFileName) + ".json"

            print('File: ', str(indexFile))
            print('Config: ', str(indexConfig))

            # Initialize DocumentStore
            document_store = FAISSDocumentStore(sql_url=sqlite_path)

            libName = "vectorDB/" + str(vectorDBFileName) + '.faiss'

            document_store.write_documents(documents)

            # Initialize Retriever
            retriever = DensePassageRetriever(document_store=document_store,
                                              query_embedding_model=queryModel,
                                              passage_embedding_model=passageModel,
                                              use_gpu=False)

            document_store.update_embeddings(retriever=retriever)

            document_store.save(index_path=libName, config_path="vectorDB/" + str(vectorDBFileName) + ".json")

            print('*'*120)
            print('Testing with RAG & OpenAI...')
            print('*'*120)

            answer = self.ragAnswerWithHaystackAndGPT3(strVal, retriever)

            print('*'*120)
            print('Testing Answer:: ')
            print(answer)
            print('*'*120)

            return 0

        except Exception as e:
            x = str(e)
            print('Error: ', x)

            return 1
