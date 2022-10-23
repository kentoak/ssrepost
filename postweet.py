#from getwilog import GetTwilog
import sys
sys.path.append('/usr/local/lib/python3.9/site-packages') #pip show tweepyで出た。
#pprint.pprint(sys.path)
import twitterAPIConfig
import tweepy
import time

def main():
    ConK,ConSK,AccT,AccST,Bear = (
        twitterAPIConfig.CONSUMER_KEY,
        twitterAPIConfig.CONSUMER_SECRET,
        twitterAPIConfig.ACCESS_TOKEN,
        twitterAPIConfig.ACCESS_TOKEN_SECRET,
        twitterAPIConfig.Bearer
    )
    auth = tweepy.OAuthHandler(ConK,ConSK)
    auth.set_access_token(AccT, AccST)
    t = tweepy.API(auth)
    urls=[]
    texts=[]
    onlyTxt=[]
    onlytxt=[]
    onlyLink=[]
    repostText=[]
    #tweetsFromSSrepost = tweepy.Cursor(t.search_tweets,q='http',id="ssrepost",tweet_mode='extended',include_entities=True,result_type='recent',lang='en').items(100)
    tweetsFromSSrepost = tweepy.Cursor(t.user_timeline,user_id="ssrepost",tweet_mode='extended').items(500)
    for tweet in tweetsFromSSrepost:
        if len(tweet.entities['urls'])>0:
            if hasattr(tweet,"full_text"):
                if "http" in tweet.full_text[:tweet.full_text.find('http')-1]:
                    continue
                repostText.append(tweet.full_text[:tweet.full_text.find('http')-1].lower().replace('&amp;','&').replace('’','\''))
        else:
            if tweet.full_text[:2] == "RT":
                print("引用リツイート")
            else:
                print("Linkなし！",tweet.full_text.replace('&amp;','&').replace('’','\''))
                repostText.append(tweet.full_text.lower().replace('&amp;','&').replace('’','\''))
    
    print(repostText)
    #print("tao")
    tweetsFromSS = tweepy.Cursor(t.user_timeline,id="swimswamnews",tweet_mode='extended',include_entities=True).items(100)
    for tw in tweetsFromSS:
        if len(tw.entities['urls'])>0:
            if hasattr(tw,"full_text"):
                onlyLink.append(tw.entities['urls'][0]['expanded_url'])
                onlyTxt.append(tw.full_text[:tw.full_text.find('http')-1].replace('&amp;','&').replace('’','\''))
                onlytxt.append(tw.full_text[:tw.full_text.find('http')-1].lower().replace('&amp;','&').replace('’','\''))
        else:
            if tw.full_text[:2] == "RT":
                print("引用リツイート")
            else:
                print("Linkなし！",tw.full_text[:tw.full_text.find('http')-1].replace('&amp;','&').replace('’','\''))
                onlyLink.append("nolink")
                onlyTxt.append(tw.full_text.replace('&amp;','&').replace('’','\''))
                onlytxt.append(tw.full_text.lower().replace('&amp;','&').replace('’','\''))
    urls.reverse()
    texts.reverse()
    onlyTxt.reverse()
    onlytxt.reverse()
    onlyLink.reverse()
    # print(onlyLink)
    # print(onlytxt)
    # print(repostText)
    
    for i in range(len(onlyLink)):
        T=onlyTxt[i]
        txt=onlyTxt[i].lower()
        link=onlyLink[i]
        print("now is ",i)
        #print("\n",T,"\n",link)
        print(onlytxt[i+1:].count(txt),repostText.count(txt))
        if onlytxt[i+1:].count(txt)==0 and repostText.count(txt)==0:
            print(txt,"is new one !!!")
            if link=="nolink":
                t.update_status(status=T)
                print("Linkなしバージョン",T)
            else:
                if "ow.ly/" in link:
                    t.update_status(status=T+'\n'+link)
                else:
                    t.update_status(status=T+'\n'+link[:-1])
            time.sleep(10)
    print("Done")

if __name__=="__main__":
    main()
