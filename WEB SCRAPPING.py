#!/usr/bin/env python
# coding: utf-8

# In[282]:


#IMPORTING THE DEPENDENCIES

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import nltk.data
from IPython.display import FileLink


# ## GETTING THE SINGLE HTML/URL

# In[10]:


url="https://insights.blackcoffer.com/ai-in-healthcare-to-improve-patient-outcomes/"
r=requests.get(url)
print(r)


# In[11]:


print(r.text)


# In[12]:


contenthtml=r.text #// r.content


# ## PARSER THE HTML

# In[13]:


soup= BeautifulSoup(contenthtml , 'lxml')
print(soup.prettify)


# ## WEB SCRAPPING

# In[14]:


#to print all H1 tag in html
print(soup.find_all('h1')) #this returns a list


# In[15]:


soup.find_all('h1')[0].text #this returns the text of the first element in the list


# In[16]:


# to print all h3 tags in html
len(soup.find_all('h3'))


# In[17]:


for i in soup.find_all('h3'):
    print(i.text.strip())


# In[18]:


to print all p tags in the html
print(soup.find_all('p'))


# In[20]:


#for storing all p tags element in a list
para=[]
for i in soup.find_all('p'):
     para.append(i.text)
     


# In[21]:


print(para)


# In[22]:


#printing title of the page
title=(soup.title)
#print(title)


# In[24]:


print(title)


# In[25]:


#for exctracting the div of class 'tdb-block-inner td-fix-index'
para=[]
for i in soup.find_all('div', class_='tdb-block-inner td-fix-index'):
     para.append(i.text)
     print(i.text)


# # COMMENCEMENT OF THE PROJECT 

# In[27]:


# importing the csv file
df=pd.read_csv("C:/Users/HP/Downloads/Input.xlsx - Sheet1.csv")


# In[28]:


df


# In[29]:


df.isnull().sum()


# In[30]:


df.head()


# In[31]:


# to print each url in the file
for i in df['URL']:
    print(i)


# ## to get title of each of the URLs

# In[32]:


#to get title of each of the URLs
text=[]
for i in df['URL']:
    r=requests.get(i)
    soup=BeautifulSoup(r.content, 'html.parser')
    text.append(soup.title.text)


# In[33]:


print(text)


# In[34]:


soup=BeautifulSoup(r.content, 'html.parser')


# In[35]:


df


# In[36]:


#to print title of each URLs
d={'URL': df['URL'],'title':text}


# In[37]:


df=pd.DataFrame(d)


# In[38]:


df


# In[39]:


get_ipython().system('NotebookApp.iopub_data_rate_limit=100000000')


# ## To get text from all 'p's/ paras of each URL

# In[40]:


#to get all text from each URLs
para=[]

for i in df['URL']:
    r=requests.get(i)
    soup=BeautifulSoup(r.content, 'html.parser')
    para_text=""
    for j in soup.find_all('p'):
        para_text+=j.text
    para.append(para_text)


# In[83]:


print(para)


# In[43]:


d2={'URL': df['URL'],'title':text, 'content_para':para}
df3=pd.DataFrame(d2)


# In[44]:


df3


# In[58]:


df3['content_para'][5]


# ## To concatenate both title and text into one

# In[65]:


#to add the concatenated column
d5={'URL': df['URL'], 'both': df3['title'] + " - " + df3['content_para'] }


# In[66]:


#to add the concatenated column to the dataframe
df4=pd.DataFrame(d5)


# In[67]:


df4


# In[68]:


df4['both'][5]


# In[41]:


# another way to concatenate the text and title columns
#total_content=[]
#for i in range(len(df['URL'])):
    #total_content.append(text[i]+"-" + para[i])
    


# In[46]:


##d3={'URL': df['URL'],'tt':total_content}
#df_new=pd.DataFrame(d3)


# In[47]:


#df_new


# In[69]:


#installing library for natural language processing
get_ipython().system('pip install nltk')


# In[70]:


#to downoad the stopwords
import nltk
nltk.download('stopwords')


# In[110]:


# to tokenize the text
import nltk
nltk.download('punkt')


# In[71]:


#creating object of PorterStemmer for stemming the text
port_stem=PorterStemmer()


# In[75]:


#for stemming the text 
for content in df4['both']:
    def stemming(content):
        stemmedcontent=re.sub('[^a-zA-Z.]',' ' , content) #remove all the characters except words and full stop
        stemmedcontent=stemmedcontent.lower()             #convert the text into lower case
        stemmedcontent=stemmedcontent.split()             #splitting the text so that it can be used to remove stopwords
        stemmedcontent=[port_stem.stem(word) for word in stemmedcontent if word not in stopwords.words('english')] #to remove stopwords from the text
        stemmedcontent=' '.join(stemmedcontent)           # to join the data that was split
        return stemmedcontent


# In[77]:


df4['both']=df4['both'].apply(stemming)                  #applied function 


# In[78]:


#data frame after stemming the text
df4                 


# In[174]:


#tokenize the text of each text corresponding to espective URLs
tokenize=[]
for text in df4['both']:
    tokenize.append(word_tokenize(text))


# In[176]:


tokenize


# In[132]:


#adding tokenized text to the dataframe
df4["tokenized_text"]=tokenize


# In[135]:


df4


# ## Postive words count

# In[133]:


#importing positive and negative words
positive=pd.read_csv("C:/Users/HP/Downloads/positive-words.txt")


# In[154]:


#converting data frame to list so that it can be iterated for counting the positive words 
post=[]
for i in positive['a+']:
    post.append(i)


# In[155]:


post


# In[201]:


#counting positive words in the text 
count_words=[]
for sentence in tokenize:
    count=0
    for word in sentence:
        if word in post:
            count+=1
    count_words.append(count)
            
        


# In[209]:


len(count_words)


# In[210]:


#adding positive words score to the dataframe
df4['positive_score']=count_words


# In[206]:


df4


# ## Negative words count

# In[104]:


#importing negative words 
negative=pd.read_csv("C:/Users/HP/Downloads/negative-words.txt", encoding="latin-1" ) #encoding error


# In[105]:


negative


# In[207]:


#converting data frame to list so that it can be iterated for counting the positive words 
negt=[]
for i in negative['2-faced']:
    negt.append(i)


# In[208]:


negt


# In[215]:


count_words_negt=[]
for sentence in tokenize:
    count=0
    for word in sentence:
        if word in negt:
            count+=1
    count_words_negt.append(count)
            


# In[216]:


len(count_words)


# In[217]:


#adding negative score to the dataframe
df4['negative_score']=count_words_negt


# In[218]:


df4


# ## Polarity score

# In[232]:


#calculating the polarity score using the measure given
Polarity_Score=[]
for i in range(len(df4)):
    Polarity_Score.append((df4['positive_score'][i]-df4['negative_score'][i])/((df4['positive_score'][i]+df4['negative_score'][i])+0.000001))


# In[233]:


Polarity_Score


# In[234]:


#adding polarity score the dataframe
df4['polarity_score']=Polarity_Score


# In[235]:


df4


# ## SUBJECTIVITY SCORE

# In[238]:


##calculating the subjectivity score using the measure given
Subjectivity_Score=[]
for i in range(len(df4)):
    Subjectivity_Score.append((df4['positive_score'][i]-df4['negative_score'][i])/((len(df4['tokenized_text'][i]))+ 0.000001))


# In[239]:


Subjectivity_Score


# In[240]:


#adding subjectvity score to the dataframe
df4['Subjectivity_Score']=Subjectivity_Score


# In[241]:


df4


# ## Calculate words

# In[243]:


#calculate words in para
count_words=[]
for sentence in tokenize:
    count=0
    for word in sentence:
        count+=1
    count_words.append(count)



# In[244]:


count_words


# In[253]:


#adding words to the dataframe
df4['wordcount']=count_words


# In[254]:


df4


# In[263]:


df4.drop(['len'], axis=1)


# ## Creating the output excel file

# In[264]:


output=pd.DataFrame()


# In[267]:


d_final={'URL': df4['URL'], 'Text_and_title': df4['both'], 'Tokenized_text': df4['tokenized_text'], 'Positive_score':df4['positive_score'], 'Negative_score': df4['negative_score'], 'polarity_score':df4['polarity_score'],'Subjectivity_Score':df4['Subjectivity_Score'], 'wordcount':df4['wordcount']}


# In[268]:


output=pd.DataFrame(d_final)


# In[269]:


output


# In[277]:


#  with open("Output.csv", 'a') as f:
# output.to_csv(f)
  #  f.download('Output.csv')###


# In[283]:


output.to_csv('output.csv', index=False)


# In[284]:


FileLink('output.csv').html_link


# In[ ]:




