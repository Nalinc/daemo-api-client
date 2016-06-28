import sys

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_sse import sse
from twitter import *

sys.path.append('/Users/shirish.goyal/code/daemo-api-client/')

from daemo.client import Client

CLIENT_ID = "7ntg6edsTmKtg29uxsDazjAQfQDmmGmOXpbwQZjR"
ACCESS_TOKEN = "S9O8h8sQwCBE2bHzmmeNKDBwMZnEmH"
REFRESH_TOKEN = "nmCTCAkmoiGgl9vbSGJWbBgMlNIGJ0"

PROJECT_ID = 47

TW_CONSUMER_KEY = 'DsrLkapnW62Jh9CrSGowhHrFz'
TW_CONSUMER_SECRET = '2GqubzcNN11x3P3IZjDgL2wRW0tERzG1rG67ydmVR5Uh0Ctk4E'
TW_ACCESS_TOKEN = '746086097109688320-F46uQCNnFiZOUki8EfbAZpzrIoUUbxS'
TW_ACCESS_TOKEN_SECRET = 'aGUiYsBAYyS9J3uTU4sZl4dID9PcpnUUZOEX5YKDAEoJL'
TWITTER_ID = '1339835893'
TWITTER_NAME = 'HillaryClinton'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config["REDIS_URL"] = "redis://localhost:6379/1"
app.register_blueprint(sse, url_prefix='/stream')


def approve(result):
    print result
    return True


def completed(result):
    assert result is not None and result.get('results', None) is not None

    text = result.get('results')[0].get('result')

    if len(text) > 10:
        auth = OAuth(
            consumer_key=TW_CONSUMER_KEY,
            consumer_secret=TW_CONSUMER_SECRET,
            token=TW_ACCESS_TOKEN,
            token_secret=TW_ACCESS_TOKEN_SECRET
        )
        twitter = Twitter(auth=auth)
        twitter.statuses.update(status=text)


class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(256))
    results = db.relationship('TweetResult',
                              backref=db.backref('tweet'), lazy='dynamic')


class TweetResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(256))
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweet.id'))


class TwitterClient(object):
    def __init__(self):
        self.auth = OAuth(
            consumer_key=TW_CONSUMER_KEY,
            consumer_secret=TW_CONSUMER_SECRET,
            token=TW_ACCESS_TOKEN,
            token_secret=TW_ACCESS_TOKEN_SECRET
        )
        #
        # self.stream = TwitterStream(auth=self.auth)
        # self.iterator = self.stream.statuses.filter(follow=TWITTER_ID)
        self.client = Client(client_id=CLIENT_ID, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)
        # self.client2 = Client(client_id=CLIENT_ID, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)

        # thread = threading.Thread(target=self.run, args=())
        # thread.daemon = True
        # thread.start()

        self.client.publish(project_id=PROJECT_ID, approve=approve, completed=completed, stream=True)

    def run(self):
        for message in self.iterator:
            if message.get('text', None) is not None \
                    and 'RT' not in message.get('text'):  # \
                # and message.get('user') is not None \
                # and message.get('user').get('id', 0) == int(TWITTER_ID):
                text = message.get('text')
                # with app.app_context():
                #     print "got new tweet: %s" % text
                #
                #     prefix = '@%s ' % TWITTER_NAME
                #     if text.lower().startswith(prefix.lower()) and len(text) > 40:
                #         text = text[len(prefix):]
                #
                #     # check if tweet already in db
                #     tweet = Tweet.query.filter_by(text=text).first()
                #     if tweet is None:
                #         # tweet not in db
                #         tweet = Tweet(text=text)
                #         db.session.add(tweet)
                #         db.session.commit()
                #
                #         sse.publish({"message": text, "id": tweet.id}, type='tweet')
                #
                #         self.client2.add_data(project_id=PROJECT_ID, data={"tasks": [{
                #             "tweet": text, "id": tweet.id
                #         }]})


@app.route('/')
def home():
    tweets = Tweet.query.all()
    return render_template('home.html', tweets=tweets)


twitter_client = TwitterClient()

'''
{
  u'favorited':False,
  u'contributors':None,
  u'truncated':False,
  u'text':u'@realDonaldTrump We need to purge more self centered pompous people like him whose main interest is his own ideological purity than country.',
  u'is_quote_status':False,
  u'in_reply_to_status_id':747027629652443136,
  u'user':{
    u'follow_request_sent':None,
    u'profile_use_background_image':True,
    u'default_profile_image':True,
    u'id':3741826576,
    u'verified':False,
    u'profile_image_url_https':    u'https://abs.twimg.com/sticky/default_profile_images/default_profile_5_normal.png',
    u'profile_sidebar_fill_color':u'DDEEF6',
    u'profile_text_color':u'333333',
    u'followers_count':141,
    u'profile_sidebar_border_color':u'C0DEED',
    u'id_str':u'3741826576',
    u'profile_background_color':u'C0DEED',
    u'listed_count':18,
    u'profile_background_image_url_https':    u'https://abs.twimg.com/images/themes/theme1/bg.png',
    u'utc_offset':None,
    u'statuses_count':5147,
    u'description':None,
    u'friends_count':43,
    u'location':None,
    u'profile_link_color':u'0084B4',
    u'profile_image_url':    u'http://abs.twimg.com/sticky/default_profile_images/default_profile_5_normal.png',
    u'following':None,
    u'geo_enabled':False,
    u'profile_background_image_url':    u'http://abs.twimg.com/images/themes/theme1/bg.png',
    u'name':u'b.b',
    u'lang':u'en',
    u'profile_background_tile':False,
    u'favourites_count':10808,
    u'screen_name':u'becker_berta',
    u'notifications':None,
    u'url':None,
    u'created_at':    u'Tue Sep 22 19:20:12    +0000 2015',
    u'contributors_enabled':False,
    u'time_zone':None,
    u'protected':False,
    u'default_profile':True,
    u'is_translator':False
  },
  u'filter_level':u'low',
  u'geo':None,
  u'id':747171519097278464,
  u'favorite_count':0,
  u'lang':u'en',
  u'entities':{
    u'user_mentions':[
      {
        u'id':25073877,
        u'indices':[
          0,
          16
        ],
        u'id_str':u'25073877',
        u'screen_name':u'realDonaldTrump',
        u'name':u'Donald J. Trump'
      }
    ],
    u'symbols':[

    ],
    u'hashtags':[

    ],
    u'urls':[

    ]
  },
  u'in_reply_to_user_id_str':u'25073877',
  u'retweeted':False,
  u'coordinates':None,
  u'timestamp_ms':u'1466974546585',
  u'source':  u'<a href="http://twitter.com/#!/download/ipad" rel="nofollow">Twitter for iPad</a>',
  u'in_reply_to_status_id_str':u'747027629652443136',
  u'in_reply_to_screen_name':u'realDonaldTrump',
  u'id_str':u'747171519097278464',
  u'place':None,
  u'retweet_count':0,
  u'created_at':  u'Sun Jun 26 20:55:46  +0000 2016',
  u'in_reply_to_user_id':25073877
}
'''
