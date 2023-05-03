# Import modules and libraries
import json
from .nltk_funcs import tokenize, stem, bag_of_words
from nltk.corpus import stopwords
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from .model import NeuralNetwork

import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

def train():

    # Get the absolute path of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path of the dataset.json file
    dataset_path = os.path.join(script_dir, 'dataset.json')

    # Initialize dataset based off of torch dataset
    class ChatDataset(Dataset):
        # Constructor for samples and input/output vectors
        def __init__(self):
            self.n_samples = len(x_train)
            self.x_data = x_train
            self.y_data = y_train

        # Function to get an (input,output) pair
        def __getitem__(self, index):
            return self.x_data[index], self.y_data[index]

        # Function to return the number of samples
        def __len__(self):
            return self.n_samples

    # Open JSON file containing data, read through, and save data to dictionary
    with open(dataset_path, 'r') as f:
        data = json.load(f)

    # Initialize variables for tags and sentence data
    all_words = []
    tags = []
    pattern_tags = []

    # For line of tag block in the data list
    for data_line in data['data']:
        tag = data_line['tag'] # save tag
        tags.append(tag)
        # For each sentence in the tag block
        for pattern in data_line['patterns']:
            w = tokenize(pattern) # Tokenize sentence
            all_words.extend(w)
            pattern_tags.append((w, tag)) # Add (tokenized string, tag) tuple to list

    ignore_punct = ['?', '!', '.', ':', ';', ','] # List of punctuation to be ignored
    all_words = [stem(w) for w in all_words if w in all_words if w not in ignore_punct or stopwords.words('english')] # Replace the list of all words with only stemmed words that contain value
    # Create a distinct sorted set of words and tags
    all_words = sorted(set(all_words))
    tags = sorted(set(tags))

    # Create input and output vectors
    x_train = []
    y_train = []

    # For sentence and tag in list of tuples
    for (pattern_sentence, tag) in pattern_tags:
        bag = bag_of_words(pattern_sentence, all_words) # Create bag of words based off of sentence
        x_train.append(bag) # Append bag of words to input vector
        label = tags.index(tag) # Find index value of tag
        y_train.append(label) # Append index value of tag to output vector

    # Convert vectors to a numpy array
    x_train = np.array(x_train)
    y_train = np.array(y_train)

    # Initialize super parameters
    batch_size = 3
    hidden_size = 10
    output_size = len(tags)
    input_size = len(all_words)
    learning_rate = 0.001
    num_epochs = 1800

    # Create dataset for chatbot
    dataset = ChatDataset()
    # List of tuples containing data for chatbot
    train_loader = DataLoader(dataset = dataset, batch_size = batch_size, shuffle = True)

    # Initialize Neural Network model from class for feedforward training
    model = NeuralNetwork(input_size, hidden_size, output_size)

    # Initialize variable for Cross Entropy Loss and Softmax functions to be used for error calculations
    cross_entropy = nn.CrossEntropyLoss()
    # Set up process for updating weights/gradient
    optimizer = torch.optim.Adam(model.parameters(),learning_rate)

    # For an epoch
    for epoch in range(num_epochs):
        # For each training pair
        for (words, labels) in train_loader:
            outputs = model(words) # Feedforward output (y_predicted)
            loss = cross_entropy(outputs, labels) # Calculate cross entropy loss ((y_predicted - y)**2).mean(), where y_predicted is the expected output and y is actual output, and softmax of output
            optimizer.zero_grad() # Clears gradient for this iteration
            loss.backward() # Calculates gradient using chain rule
            optimizer.step() # Updates weights based on back propagation, ready for next epoch
        
        # Prints out current Cross Entropy Loss every 100 epochs for user
        if (epoch + 1) % 100 == 0:
            print(f'epoch {epoch+1}/{num_epochs}, loss = {loss.item():.10f}')

    print(f'Final loss, loss = {loss.item():.10f}')

    # Initialize data dictionary to save for running chatbot application
    data = {
        "model_state": model.state_dict(),
        "input_size": input_size,
        "output_size": output_size,
        "hidden_size": hidden_size,
        "all_words": all_words,
        "tags": tags
    }

    # Save data to .pth file for later use
    FILE = "satbotTA/NN/model.pth"
    torch.save(data,FILE)

    print(f'Training complete, file saved to {FILE}')
