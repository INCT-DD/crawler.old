
# coding: utf-8

# In[10]:


#Importando módulos necessários
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from datetime import datetime
import json    #Para armazenado dos dados no MongoDB

#Preenchendo as keys
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


# In[11]:


bdados=[]
class MyListener(StreamListener): #StreamListener é um objeto específico do tweepy
    def on_data(self,dados):
        tweet = json.loads(dados) #Carrega os dados em json
        created_at = tweet["created_at"]
        id_str = tweet["id_str"]
        text = tweet["text"]
        source = tweet["source"]
#        n_rt = tweet['retweet_count']
#        n_fav = tweet['favorite_count']
        name = tweet["user"]["screen_name"]
        url = "https://twitter.com/" + name + "/status/" + str(tweet['id'])
        hashtags = [i['text'] for i in tweet["entities"]["hashtags"]]
        user_mentions=[u['screen_name'] for u in tweet["entities"]['user_mentions']]
        
        obj = {'id_str':id_str, 
               'text':text,
               'name':name,
               'source':source,
               'url':url,
               'hashtags':hashtags,
               'user_mentions': user_mentions,
               'created_at':created_at
              } 
        tweetind = col.insert_one(obj).inserted_id #Cria uma coleção 'tweetind' e usa método insert_one para inserir obj nela 
        bdados.append(obj)
    
        
        return True
    


# In[12]:


#Criando meu ouvidor, um objeto da classe MyListener(), 
#e um objeto mystream, que usa minha chave de auth para acessar meu ouvidor

meuouvidor = MyListener()
mystream = Stream(auth, listener = meuouvidor) #"from tweepy import Stream"


# In[13]:


from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.brasilcombolso #Nome da coleção
col = db.tweets


# In[14]:


keywords = ["#BrasilComBolsonaro"]


# In[ ]:


while True:
        try:
            mystream.filter(track=keywords)
        except KeyError or ProtocolError:
            continue


# ### Tratando dados

# In[31]:


df['text'].drop_duplicates(inplace=True)


# In[32]:


df.info()


# In[ ]:


df


# In[45]:


df['source'] = df['source'].map(lambda x: str(x)[:-4])


# In[62]:


df['source']=df['source'].astype('category')


# In[79]:


tweetsorigi = []
for i in df['text']:
    if not i.startswith('RT'):
        tweetsorigi.append(i)

