from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from pandas.io.json import json_normalize
from mlapp.main.nlp.TrainingData import TrainingData
import mlapp.main.utilities as utils


class TextClassifier(TrainingData):

    def __init__(self, user, topic_name):
        super().__init__(user, topic_name)
        self.training_data = self.get_classified_training_data()
        self.classifier = ''
        self.count_vector = ''

    def create_classified_data_frame(self):
        data = self.training_data
        data_frame = json_normalize(data['training_data'])
        return data_frame

    def train_classier(self):
        df = self.create_classified_data_frame()
        x_train, x_test, y_train, y_test = train_test_split(df['tweet_text'], df['relevant'], random_state=0)
        count_vect = CountVectorizer()
        self.count_vector = count_vect

        x_train_counts = count_vect.fit_transform(x_train)
        tfidf_transformer = TfidfTransformer()
        x_train_tfidf = tfidf_transformer.fit_transform(x_train_counts)
        clf = MultinomialNB().fit(x_train_tfidf, y_train)
        self.classifier = clf

    def is_relevant(self, text):
        result = self.classifier.predict(self.count_vector.transform([text]))
        result = result[0]
        return result

    def get_sentiment(self, text):
        sentiment_scores = SentimentIntensityAnalyzer.polarity_scores(text)
        score = sentiment_scores['compound']
        return score
