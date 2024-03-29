from template import NaiveBayesClassifier
import csv
import re
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob
import time

def preprocess(tweet_string):
    # clean the data and tokenize it
    features = []

    # normalizing
    tweet_string = tweet_string.lower()

    # removing unicode characters
    tweet_string = re.sub(r"(@[^\s]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|http.+", "", tweet_string)

    # spell checking, it takes too long so we prefer to ignore it
    # tweet_string = TextBlob(tweet_string)
    # checked_string = str(tweet_string.correct())

    # removing stopwords
    stop_words = set(stopwords.words('english'))
    toks = word_tokenize(tweet_string)
    filtered_toks = [word for word in toks if word not in stop_words]

    features = set(filtered_toks)
    return features

def load_data(data_path):
    # load the train csv file and return the data
    data = []
    with open(data_path, mode ='r') as file:
        csvFile = csv.reader(file)
        next(csvFile)
        for line in csvFile:
            tweet = preprocess(line[2])
            data.append((tweet, line[4]))
    return data

def calculate_accuracy(data_path):
    # load the eval csv file and return accuracy
    correct_labed = 0
    total = 0
    with open(data_path, mode ='r') as file:
        csvFile = csv.reader(file)
        next(csvFile)
        for line in csvFile:
            tweet = preprocess(line[2])
            c = nb_classifier.classify(tweet)
            if(c == line[4]):
                correct_labed += 1
            total += 1

    accuray = correct_labed/total
    return accuray

def test(data_path, result_path):
    result = open(result_path, mode='w+')
    with open(data_path, mode ='r') as file:
        csvFile = csv.reader(file)
        next(csvFile)
        for line in csvFile:
            tweet = preprocess(line[2])
            c = nb_classifier.classify(tweet)
            result.write(f"{c}\n")
    result.close()

# train your model and report the duration time
train_data_path = "train_data.csv"
classes = ['positive', 'negative', 'neutral']
nb_classifier = NaiveBayesClassifier(classes)

start_time = time.time()
nb_classifier.train(load_data(train_data_path))
end_time = time.time()
elapsed_time = end_time - start_time
print("Model trained successfully!")
print(f"Train time: {elapsed_time}")

eval_accuracy = calculate_accuracy("eval_data.csv")
print("Accuracy calculated successfully!")
print(f"Accuracy: {eval_accuracy}")

test("test_data_nolabel.csv", "result.txt")
print("Test data labeled successfully!")

test_string = "I love playing football"
print(nb_classifier.classify(preprocess(test_string)))