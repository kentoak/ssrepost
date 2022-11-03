import sys
sys.path.append('/usr/local/lib/python3.9/site-packages') #pip show tweepyで出た。
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
    tweetsFromSSrepost = tweepy.Cursor(t.user_timeline,user_id="ssrepost",tweet_mode='extended').items(300)
    print("\n@ssrepost")
    for tweet in tweetsFromSSrepost:
        if len(tweet.entities['urls'])>0:
            if hasattr(tweet,"full_text"):
                if "http" in tweet.full_text[:tweet.full_text.find('http')-1]:
                    continue
                repostText.append(tweet.full_text[:tweet.full_text.find('http')-1].lower().replace('&amp;','&').replace('’','\''))
        else:
            if tweet.full_text[:2] == "RT":
                print("引用リツイート,",tweet.full_text)
            else:
                #print("Linkなし！",tweet.full_text.replace('&amp;','&').replace('’','\''))
                if "https://t.co/" in tweet.full_text:
                    repostText.append(tweet.full_text[:tweet.full_text.find("https://t.co/")].lower().replace('&amp;','&').replace('’','\''))
                else:
                    repostText.append(tweet.full_text.lower().replace('&amp;','&').replace('’','\''))

    tweetsFromSS = tweepy.Cursor(t.user_timeline,id="swimswamnews",tweet_mode='extended',include_entities=True).items(100)
    quoteIds=[]
    print("\n@SwimSwamNews")
    for tw in tweetsFromSS:
        if len(tw.entities['urls'])>0:
            if hasattr(tw,"full_text"):
                if "https://twitter.com" in tw.entities['urls'][0]['expanded_url']:
                    quoteIds.append(tw.id)
                    print("引用リツイート, ",tw.full_text)
                elif tw.full_text[:2] == "RT":
                    print("リツイート（リンクあり）, ",tw.full_text)
                else:
                    onlyLink.append(tw.entities['urls'][0]['expanded_url'])
                    onlyTxt.append(tw.full_text[:tw.full_text.find('http')-1].replace('&amp;','&').replace('’','\''))
                    onlytxt.append(tw.full_text[:tw.full_text.find('http')-1].lower().replace('&amp;','&').replace('’','\''))
        else:
            if tw.full_text[:2] == "RT":
                print("リツイート（リンクなし）, ",tw.full_text)
            elif tw.in_reply_to_status_id:
                print("リプライ, ",tw.in_reply_to_status_id)
            else:
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
        print(onlytxt[i+1:].count(txt),repostText.count(txt))
        newTweetflag=False
        if "https://t.co/" in txt:
            print("画像系ツイート")
            print(txt[:txt.find("https://t.co/")],repostText.count(txt[:txt.find("https://t.co/")]))
            if onlytxt[i+1:].count(txt[:txt.find("https://t.co/")])==0 and repostText.count(txt[:txt.find("https://t.co/")])==0:   
                print(onlytxt[i+1:].count(txt[:txt.find("https://t.co/")]),repostText.count(txt[:txt.find("https://t.co/")]))    
                newTweetflag=True
        else:
            if onlytxt[i+1:].count(txt)==0 and repostText.count(txt)==0:
                print(onlytxt[i+1:].count(txt),repostText.count(txt))
                newTweetflag=True
        if newTweetflag:
            print(txt,"is new one !!!")
            if link=="nolink":
                #t.update_status(status=T)
                print("Linkなしバージョン",T)
            else:
                if "ow.ly/" in link:
                    #t.update_status(status=T+'\n'+link)
                    print(T+'\n'+link)
                if "twitter.com" in link:
                    print("引用リツイートなのでツイートしません")
                    #print(T+'\n'+link)
                else:
                    #t.update_status(status=T+'\n'+link[:-1])
                    print(T+'\n'+link[:-1])
            time.sleep(10)
    print("Done")

if __name__=="__main__":
    main()
