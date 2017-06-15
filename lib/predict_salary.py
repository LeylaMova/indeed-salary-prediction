#!/Users/Leyla/anaconda/bin/python
import pandas as pd
import numpy as np
import json
import tflearn
from sklearn.feature_extraction import stop_words
from lib.preprocess import preprocess_wo_salary


with open('data/vocab.json', 'r') as infile:
    vocab = json.load(infile)
        
with open('data/word2idx.json', 'r') as infile:
    word2idx = json.load(infile)
    
# Load a model
model.load('model/model.tflearn')


def text_to_vector(text):
        
    word_vec = np.zeros((1, len(vocab)))
    for word in text.split():
        if word in word2idx.keys():
            word_vec[0][word2idx[word]] += 1
            
    return np.array(word_vec)


def predict_salary(df):
    
    salary = {'0':'below $66000', '1':'$66000 to $150000', '2':'above $150000'}
    
    texts = df['text'].values
    
    test_vectors = np.zeros((len(texts), len(vocab)), dtype=np.int_)
    for ii, text in enumerate(texts):
        test_vectors[ii] = text_to_vector(text)
        
    df['predicted_salary_class'] = np.argmax(np.array(model.predict(test_vectors)), axis=1)
    df['predicted_salary_range'] = df['predicted_salary_class'].apply(lambda x: salary[str(x)] if str(x) in salary.keys() else None)
    
    return df
    
    
    
    

    