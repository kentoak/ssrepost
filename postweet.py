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
    tweetsFromSSrepost = tweepy.Cursor(t.user_timeline,user_id="ssrepost",tweet_mode='extended').items(1000)
    print("@ssrepost")
    for tweet in tweetsFromSSrepost:
        if len(tweet.entities['urls'])>0:
            if hasattr(tweet,"full_text"):
                if "http" in tweet.full_text[:tweet.full_text.find('http')-1]:
                    print("本文なしリンクのみ",tweet.full_text[:tweet.full_text.find('http')-1],tweet.entities['urls'][0]['expanded_url']) 
                    repostText.append(tweet.entities['urls'][0]['expanded_url'])
                else:
                    repostText.append(tweet.full_text[:tweet.full_text.find('http')-1].lower().replace('&amp;','&').replace('’','\''))
        else:
            if tweet.full_text[:2] == "RT":
                print("引用リツイート")
            else:
                #print("Linkなし！",tweet.full_text.replace('&amp;','&').replace('’','\''))
                if "https://t.co/" in tweet.full_text:#リンクなしの画像ツイート
                    print("リンクなしの画像ツイート",tweet.full_text[:tweet.full_text.find("https://t.co/")])
                    repostText.append(tweet.full_text[:tweet.full_text.find("https://t.co/")].lower().replace('&amp;','&').replace('’','\''))
                else:
                    repostText.append(tweet.full_text.lower().replace('&amp;','&').replace('’','\''))


    #print("repostList is \n",repostText)
    #print("tao")
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
                elif "http" in tw.full_text[:tw.full_text.find('http')-1]:
                    onlyTxt.append(tw.full_text[:tw.full_text.find('http')-1])
                    onlyLink.append(tw.entities['urls'][0]['expanded_url'])
                    onlytxt.append(tw.full_text[:tw.full_text.find('http')-1])
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
                #print("Linkなし！",tw.full_text.replace('&amp;','&').replace('’','\''))
                onlyLink.append("nolink")
                # if "https://t.co/" in tw.full_text:
                #     onlyTxt.append(tw.full_text[:tw.full_text.find("https://t.co/")].replace('&amp;','&').replace('’','\''))
                #     onlytxt.append(tw.full_text[:tw.full_text.find("https://t.co/")].lower().replace('&amp;','&').replace('’','\''))
                # else:
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
    print("#############################")
    for i in range(len(onlyLink)):
        T=onlyTxt[i]
        txt=onlyTxt[i].lower()
        link=onlyLink[i]
        print("now is ",i,T)
        #print("\n",T,"\n",link)
        print(onlytxt[i+1:].count(txt),repostText.count(txt))
        newTweetflag=False
        if "https://t.co/" in txt:
            print("画像系ツイート",T,txt,link)
            print("repostでツイートされているか",txt[:txt.find("https://t.co/")],repostText.count(txt[:txt.find("https://t.co/")]),link[:-1] in repostText)
            if onlytxt[i+1:].count(txt[:txt.find("https://t.co/")])==0 and repostText.count(txt[:txt.find("https://t.co/")])==0 and repostText.count(link[:-1])==0:   
                print("(SwimSwamでのツイートの数,repostでの当該ツイートの数)",onlytxt[i+1:].count(txt[:txt.find("https://t.co/")]),repostText.count(link[:-1])) 
                newTweetflag=True
        else:
            if onlytxt[i+1:].count(txt)==0 and repostText.count(txt)==0:
                print(onlytxt[i+1:].count(txt),repostText.count(txt))
                newTweetflag=True
        if newTweetflag:
            print(T,"is new one !!!")
            if link=="nolink":
                t.update_status(status=T)
                print("Linkなしバージョン",T)
            else:
                if "ow.ly/" in link:
                    t.update_status(status=T+'\n'+link)
                    print(T+'\n'+link)
                elif "twitter.com" in link:
                    print("引用リツイートなのでツイートしません")
                    #print(T+'\n'+link)
                else:
                    print(T+' '+link[:-1])
                    if "https://t.co/" in T:
                    	t.update_status(status=link[:-1])
                    else:
                    	t.update_status(status=T+'\n'+link[:-1])
            time.sleep(10)
        # if onlyTxt[i+1:].count(txt)==0 and repostText.count(txt)==0:
        #     print(txt,"is new one !!!")s
        #     if "ow.ly/" in link:
        #         t.update_status(status=T+'\n'+link)
        #     else:
        #         t.update_status(status=T+'\n'+link[:-1])
        #     time.sleep(10)

        # with open("swimswamnews_Tweet.txt",encoding = "utf-8",mode = "r") as f:
        #     for row in f:
        #         url,text = row.split("\t")
        #         urls.append(url)
        #         texts.append(text)
        #         onlyTxt.append(text[:text.find('http')-1].lower())
        
        # with open("ssrepost_Tweet.txt",encoding = "utf-8",mode = "r") as f:
        #     for row in f:
        #         url,text = row.split("\t")
        #         repostText.append(text[:text.find('http')].lower())
        # print(repostText)
    print("Done")

if __name__=="__main__":
    main()
