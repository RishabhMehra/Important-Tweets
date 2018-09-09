from flask import Flask, render_template, request,flash,url_for,redirect
import add
app = Flask(__name__)

@app.route('/')
def index():
   return render_template('init.html')

@app.route('/handle_data', methods = ['POST', 'GET'])
def handle_data():
	userQuestion = request.form['userQuestion']
	ad=str(userQuestion)
	return render_template('result.html',query=userQuestion, hi = search(ad).to_html())

	



def search(text):
    import nltk
    import re
    import tweepy
    from textblob import TextBlob
    import re
    import pandas as pd

    consumer_key = <<Enter your Key>>
    consumer_secret = <<Enter your Key>>'
    access_token = <<Enter your Key>>'
    access_token_secret = <<Enter your Key>>'
    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api=tweepy.API(auth)
    public_tweets = api.search(text,tweet_mode='extended',count=100)

    data_df = pd.DataFrame([{"date": x.created_at,
                             "text": x.full_text,
                             "user": x.user.screen_name,
                             "followers":x.user.followers_count,
                             "Verified": x.user.verified,
                             "id": x.id} for x in public_tweets])


    retweet=list()

    for x in data_df.text:
        if re.match(r'^RT', x):
            retweet.append(0)
        else:
            retweet.append(1)
    #0- Retweet
    #1- No Retweet

    data_df['retweet']=retweet

    mention=[]
    for x in data_df['text']:
        l=re.search(r"(@[A-Za-z0-9]+)",x)
        if l:
            h=l.group(0)
            mention.append(h)
        else :
            mention.append(None)

    allmen=[]
    for x in data_df['text']:
        k=re.findall(r"(@[A-Za-z0-9]+)",x)
        allmen.append(k)

    allhash=[]
    for x in data_df['text']:
        k=re.findall(r"(#[A-Za-z0-9]+)",x)
        allhash.append(k)

    links=[]

    for tweet in data_df['text']:
        urls = re.search('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', tweet)
        if urls:
                try:
                    res = urllib2.urlopen(urls)
                    actual_url = res.geturl()
                    links.append(actual_url)
                except:
                    links.append(urls)
        else:
            links.append(None)


    data_df['Mentions']=allmen
    data_df['links']=links
    data_df['Hashtags']=allhash

    def process_tweet(tweet):
        return " ".join(re.sub("(@[A-Za-z0-9]+)", " ",tweet.lower()).split())
    def remrt(tweet):
        return re.sub(r"^rt"," ",tweet)

    data_df['ctweets']=data_df['text'].apply(process_tweet)
    data_df['ctweets']=data_df['ctweets'].apply(remrt)

    def linkrem(tweet):
         return re.sub(r"http\S+", "", tweet)
    data_df['ctweets1']=data_df['ctweets'].apply(linkrem) 

    # remove punctuations
    data_df['ctweets2']=data_df['ctweets1'].str.replace("[^a-zA-Z#]"," ")

    del data_df['ctweets1']

    del data_df['ctweets']

    #kiki challenge

    data_df=data_df.sort_values(by='followers', ascending=False)

    data_df=data_df.groupby(['followers', 'retweet', 'date'], sort=False).max().reset_index()

    data_df[data_df.followers==512564].ctweets2.str.len()

    data_df['length'] = data_df.ctweets2.str.len()

    data_df['score']= data_df.followers/data_df.followers.max()*0.9 + data_df.length/data_df.length.max()*0.05 + data_df.retweet/data_df.retweet.max()*0.05

    data_df=data_df.sort_values(by='score', ascending=False)
    
    data_df=data_df.head(20)
    columns=['user','text']
    disp_df=data_df[columns]	
    pd.set_option('display.max_colwidth', -1)
    return disp_df	
	
	
	
if __name__ == '__main__':
   app.run(debug = True)

	
def add_to_10(a):
	#userQuestion = request.form['userQuestion']
	c='10'+a
	return c
	
if __name__ == '__main__':
   app.run()
