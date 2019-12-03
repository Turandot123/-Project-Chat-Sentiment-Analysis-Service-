import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier

import re, string, random


def download_corpora():
    ''' Downloads data you need to train model''' 
    nltk.download('stopwords')
    nltk.download('twitter_samples')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')
    nltk.download('punkt')


def remove_noise(tweet_tokens, stop_words=()):
    ''' cleans the messages and removes unnecessary symbols, expressions'''
    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|' \
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', token)
        token = re.sub("(@[A-Za-z0-9_]+)", "", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens


def get_all_words(cleaned_tokens_list):
    ''' passes a list of strings and returns a word from each list ''' 
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token 


def get_tweets_for_model(cleaned_tokens_list):
    ''' generates a dictionary when iterating through a list of tokens '''
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)


class Sentiment:
    '''Parses, cleans and uses the NLTK tweets corpora to train a NaiveBayesClassifier to
    predict sentiments of English sentences'''
    def __init__(self):
        download_corpora()

        stop_words = stopwords.words('english')
        positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
        positive_cleaned_tokens_list = [remove_noise(tokens, stop_words) for tokens in positive_tweet_tokens]
        self.positive_tokens = get_tweets_for_model(positive_cleaned_tokens_list)

        negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')
        negative_cleaned_tokens_list = [remove_noise(tokens, stop_words) for tokens in negative_tweet_tokens]
        self.negative_tokens = get_tweets_for_model(negative_cleaned_tokens_list)

        positive_dataset = [(tweet_dict, "Positive") for tweet_dict in self.positive_tokens]
        negative_dataset = [(tweet_dict, "Negative") for tweet_dict in self.negative_tokens]
        dataset = positive_dataset + negative_dataset
        random.shuffle(dataset)
        train_data = dataset[:7000]
        # test_data = dataset[7000:]

        self.classifier = NaiveBayesClassifier.train(train_data)

    def classify(self, text):
        '''Tokenizes and cleans a sentence. Uses the classifier to predict the sentiment.'''
        tokens = remove_noise(word_tokenize(text))
        return self.classifier.classify(dict([token, True] for token in tokens))
