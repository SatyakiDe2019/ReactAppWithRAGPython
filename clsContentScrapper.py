#####################################################
#### Written By: SATYAKI DE                      ####
#### Written On: 27-May-2023                     ####
#### Modified On 28-May-2023                     ####
####                                             ####
#### Objective: This is the main calling         ####
#### python class that will invoke the           ####
#### LangChain of package to extract             ####
#### the transcript from the YouTube videos &    ####
#### then answer the questions based on the      ####
#### topics selected by the users.               ####
####                                             ####
#####################################################

from langchain.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from googleapiclient.discovery import build

import clsTemplate as ct
from clsConfigClient import clsConfigClient as cf

import os

from flask import jsonify
import requests

###############################################
###           Global Section                ###
###############################################
open_ai_Key = cf.conf['OPEN_AI_KEY']
os.environ["OPENAI_API_KEY"] = open_ai_Key
embeddings = OpenAIEmbeddings(openai_api_key=open_ai_Key)

YouTube_Key = cf.conf['YOUTUBE_KEY']
youtube = build('youtube', 'v3', developerKey=YouTube_Key)

# Disbling Warning
def warn(*args, **kwargs):
    pass

import warnings
warnings.warn = warn

###############################################
###    End of Global Section                ###
###############################################

class clsContentScrapper:
    def __init__(self):
        self.model_name = cf.conf['MODEL_NAME']
        self.temp_val = cf.conf['TEMP_VAL']
        self.max_cnt = int(cf.conf['MAX_CNT'])
        self.url = cf.conf['BASE_URL']
        self.header_token = cf.conf['HEADER_TOKEN']

    def createDBFromYoutubeVideoUrl(self, video_url):
        try:
            loader = YoutubeLoader.from_youtube_url(video_url)
            transcript = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            docs = text_splitter.split_documents(transcript)

            db = FAISS.from_documents(docs, embeddings)
            return db

        except Exception as e:
            x = str(e)
            print('Error: ', x)
            return ''


    def getResponseFromQuery(self, db, query, k=4):
        try:
            """
            gpt-3.5-turbo can handle up to 4097 tokens. Setting the chunksize to 1000 and k to 4 maximizes
            the number of tokens to analyze.
            """

            mod_name = self.model_name
            temp_val = self.temp_val

            docs = db.similarity_search(query, k=k)
            docs_page_content = " ".join([d.page_content for d in docs])

            chat = ChatOpenAI(model_name=mod_name, temperature=temp_val)

            # Template to use for the system message prompt
            template = ct.templateVal_1

            system_message_prompt = SystemMessagePromptTemplate.from_template(template)

            # Human question prompt
            human_template = "Answer the following question: {question}"
            human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

            chat_prompt = ChatPromptTemplate.from_messages(
                [system_message_prompt, human_message_prompt]
            )

            chain = LLMChain(llm=chat, prompt=chat_prompt)

            response = chain.run(question=query, docs=docs_page_content)
            response = response.replace("\n", "")
            return response, docs

        except Exception as e:
            x = str(e)
            print('Error: ', x)

            return '', ''

    def topFiveURLFromYouTube(self, service, **kwargs):
        try:
            video_urls = []
            channel_list = []
            results = service.search().list(**kwargs).execute()

            for item in results['items']:
                print("Title: ", item['snippet']['title'])
                print("Description: ", item['snippet']['description'])
                channel = item['snippet']['channelId']
                print("Channel Id: ", channel)

                # Fetch the channel name using the channel ID
                channel_response = service.channels().list(part='snippet',id=item['snippet']['channelId']).execute()
                channel_title = channel_response['items'][0]['snippet']['title']
                print("Channel Title: ", channel_title)
                channel_list.append(channel_title)

                print("Video Id: ", item['id']['videoId'])
                vidURL = "https://www.youtube.com/watch?v=" + item['id']['videoId']
                print("Video URL: " + vidURL)
                video_urls.append(vidURL)
                print("\n")

            return video_urls, channel_list

        except Exception as e:
            video_urls = []
            channel_list = []
            x = str(e)
            print('Error: ', x)

            return video_urls, channel_list

    def extractContentInText(self, topic, query):
        try:
            discussedTopic = []
            strKeyText = ''
            cnt = 0
            max_cnt = self.max_cnt

            urlList, channelList = self.topFiveURLFromYouTube(youtube, q=topic, part='id,snippet',maxResults=max_cnt,type='video')
            print('Returned List: ')
            print(urlList)
            print()

            for video_url in urlList:
                print('Processing Video: ')
                print(video_url)
                db = self.createDBFromYoutubeVideoUrl(video_url)

                response, docs = self.getResponseFromQuery(db, query)

                if len(response) > 0:
                    strKeyText = 'As per the topic discussed in ' + channelList[cnt] + ', '
                    discussedTopic.append(strKeyText + response)

                cnt += 1

            return discussedTopic
        except Exception as e:
            discussedTopic = []
            x = str(e)
            print('Error: ', x)

            return discussedTopic

    def extractCatalog(self):
        try:
            base_url = self.url
            header_token = self.header_token

            url = base_url + '/departments'

            print('Full URL: ', str(url))

            payload={}
            headers = {'Cookie': header_token}

            response = requests.request("GET", url, headers=headers, data=payload)

            x = response.text

            return x
        except Exception as e:
            discussedTopic = []
            x = str(e)
            print('Error: ', x)

            return x
