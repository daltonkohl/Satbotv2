# Import libraries
import numpy as np
import nltk
from nltk.stem import SnowballStemmer

import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

# Initialize stemmer variable with Snowball algorithm
stemmer = SnowballStemmer('english')

# Splits sentence into numpy array of strings
def tokenize(sentence):
    return nltk.word_tokenize(sentence)

# Stems words in numpy array with Porter2 (Snowball) algorithm; Root word from original word
def stem(word):
    return stemmer.stem(word.lower()) # Lowercase input word

# Generates array of 0s and 1s based off of tokenized words that occur in saved data
def bag_of_words(tokenized_sentence, words):
    sentence_words = [stem(word) for word in tokenized_sentence] # stem each word in tokenized sentence
    bag = np.zeros(len(words), dtype=np.float32) # Initialize bag with 0s for each word
    # For word in words
    for idx, w in enumerate(words):
        # If word in stemmed tokenized sentence, change array to 1 at index of word
        if w in sentence_words: 
            bag[idx] = 1

    return bag
