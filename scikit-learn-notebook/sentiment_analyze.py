#!/usr/bin/env python
# coding: utf-8

# ### Data Class

# In[16]:


class Sentiment:
    POSITIVE = 'POSITIVE'
    NEUTRAL = 'NEUTRAL'
    NEGATIVE = 'NEGATIVE'

class Review:
    def __init__(self, comment, score):
        self.comment = comment
        self.score = score
        self.sentiment = self.get_sentiment()
    
    
    def get_sentiment(self):
        if self.score > 3:
            return Sentiment.POSITIVE
        elif self.score == 3:
            return Sentiment.NEUTRAL
        else:
            return Sentiment.NEGATIVE


# ### Load Data

# In[18]:


import json

reviews = []
with open('./data/Books_small.json') as f:
    for line in f:
        review = json.loads(line)
        reviews.append(Review(review['reviewText'], review['overall']))
reviews[5].sentiment


# ### Prep Data

# In[21]:


from sklearn.model_selection import train_test_split

train, test = train_test_split(reviews, test_size=0.33, random_state=42)


# In[23]:


train_X = [x.comment for x in train]
train_y = [y.sentiment for y in train]

test_X = [x.comment for x in test]
test_y = [y.sentiment for y in test]


# #### Bag of word vectorization

# In[25]:


from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer()
train_X_vectors = vectorizer.fit_transform(train_X)

print(train_X[0])
print(train_X_vectors[0].toarray())


# ### Classification
