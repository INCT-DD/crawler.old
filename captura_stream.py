
# coding: utf-8

# In[1]:


#Importando módulos necessários
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from datetime import datetime
import json    #Para armazenado dos dados no MongoDB


# In[2]:


#Preenchendo as keys
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""


# In[3]:


#Criando a autenticação
auth = OAuthHandler(consumer_key, consumer_secret)


# In[4]:


auth.set_access_token(access_token, access_token_secret)


# In[5]:


#Criando uma classe e método para captura dos dados do Twitter e 
#armazenamento no MongoDB

class MyListener(StreamListener): #StreamListener é um objeto específico do tweepy
    def on_data(self,dados):
        tweet = json.loads(dados) #Carrega os dados em json
        created_at = tweet["created_at"]
        id_str = tweet['id_str']
        text = tweet['text']
        obj = {'created_at':created_at, 'id_str':id_str, 'text':text} #Um documendo no MongoDB
        tweetind = col.insert_one(obj).inserted_id #Cria uma coleção 'tweetind' e usa método insert_one para inserir obj nela 
        print(obj)
        return True


# In[9]:


#Criando meu ouvidor, um objeto da classe MyListener(), 
#e um objeto mystream, que usa minha chave de auth para acessar meu ouvidor

meuouvidor = MyListener()
mystream = Stream(auth, listener = meuouvidor) #"from tweepy import Stream"


# In[10]:


#CONFIGURANDO O BANCO DE DADOS PARA RECEBER OS DADOS
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.twitterdb
col = db.tweets


# In[12]:


#Estabelecendo critérios, no caso uma lista de palavras-chaves
keywords = ["#GolpeDeEstadoTSJ"]


# In[13]:


#Iniciando filtro e gravando tweets no MongoDB
mystream.filter(track=keywords)


# In[17]:


#Verificando se de fato foi criado algum documento
col.find_one()


# In[14]:


#Criando o dataset com dados retornados do MongoDB

dataset = [{'created_at': item['created_at'],
           "text": item['text'],
           } for item in col.find()]

#Para cada elemento encontrado por meio do cursor col.find(), 
#crie uma lista com os seguintes elementos.


# In[15]:


##Criando um DATAFRAME com Pandas

import pandas as pd
df = pd.DataFrame(dataset)


# In[16]:


df


# In[ ]:


#ANALISANDO DADOS COM SCIKIT LEARN

from sklearn.feature_extraction.text import CountVectorizer


# In[57]:


#Usando o método CountVectorizer para criar uma matriz de docs
cv = CountVectorizer()
count_matrix = cv.fit_transform(df.text)


# In[58]:


#Contando o número de palavras no dataset
word_count = pd.DataFrame(cv.get_feature_names(), columns = ['words'])
word_count["count"] = count_matrix.sum(axis=0).tolist()[0]
word_count = word_count.sort_values('count', ascending = False).reset_index(drop=True)
word_count[:50]

