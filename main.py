import joblib
import tweepy
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Twitter API credentials
consumer_key = "YOUR_CONSUMER_KEY"
consumer_secret = "YOUR_CONSUMER_SECRET"
access_key = "YOUR_ACCESS_KEY"
access_secret = "YOUR_ACCESS_SECRET"

# Authenticate and access Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

# Preprocessing function to clean the text
def clean_text(text):
    # Remove URLs, mentions, and hashtags
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"@\S+", "", text)
    text = re.sub(r"#\S+", "", text)
    # Remove punctuations and numbers
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\d+", "", text)
    # Convert to lowercase
    text = text.lower()
    # Remove stopwords and lemmatize words
    stopwords_list = stopwords.words("english")
    lemmatizer = WordNetLemmatizer()
    text = " ".join([lemmatizer.lemmatize(word) for word in text.split() if word not in stopwords_list])
    return text

# Get tweets and clean the text
tweets = []
for tweet in tweepy.Cursor(api.search_tweets, q="your_brand_name", lang="en").items(100):
    text = clean_text(tweet.text)
    tweets.append(text)

# Load the saved model
vectorizer = TfidfVectorizer()
clf = LogisticRegression()
vectorizer = joblib.load("vectorizer.pkl")
clf = joblib.load("clf.pkl")

# Vectorize the text and predict sentiment
X = vectorizer.transform(tweets)
y_pred = clf.predict(X)

# Print the sentiment of each tweet
for i, tweet in enumerate(tweets):
    print("Tweet:", tweet)
    print("Sentiment:", y_pred[i])
    print()
