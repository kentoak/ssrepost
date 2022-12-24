#from getwilog import GetTwilog
import sys
sys.path.append('/usr/local/lib/python3.9/site-packages') #pip show tweepyで出た。
#pprint.pprint(sys.path)
import twitterAPIConfig
import tweepy
import time
from bs4 import BeautifulSoup
import requests
import os
from twitter_text import parse_tweet
import cssutils

CONSUMER_KEY=twitterAPIConfig.CONSUMER_KEY
CONSUMER_SECRET=twitterAPIConfig.CONSUMER_SECRET
ACCESS_TOKEN=twitterAPIConfig.ACCESS_TOKEN
ACCESS_TOKEN_SECRET=twitterAPIConfig.ACCESS_TOKEN_SECRET

def post1(str,gazou):
    auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    t = tweepy.API(auth)
    filename = '/home/pi/pythonn/temp1.jpg'
    request = requests.get(gazou, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)
        t.update_status_with_media(status=str,filename=filename)
        os.remove(filename)
    else:
        print("Unable to download image")

def judge_tweetable(text):
    if parse_tweet(text).valid:
        return "ツイート可能です"
    else:
        return "ツイート不可能です"

def change_tweet_len(tweet_format, target):
    target = target[:280]
    for i in range(len(target)):
        if i == 0:
            tweet_txt = tweet_format.format(target)
        else:
            tweet_txt = tweet_format.format(target[:-i] + "…")
        if parse_tweet(tweet_txt).valid:
            return tweet_txt
    return 0
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
    repostLink=[]
    tweetsFromSSrepost = tweepy.Cursor(t.user_timeline,user_id="ssrepost",tweet_mode='extended').items(1000)
    print("@ssrepost")
    for tweet in tweetsFromSSrepost:
        if len(tweet.entities['urls'])>0:#リンクあり
            if hasattr(tweet,"full_text"):
                if "http" in tweet.full_text[:tweet.full_text.find('http')-1]:                      
                    print("本文なしリンクのみ",tweet.full_text[:tweet.full_text.find('http')-1],tweet.entities['urls'][0]['expanded_url']) 
                    repostText.append(tweet.entities['urls'][0]['expanded_url'])
                    tmplink=tweet.entities['urls'][0]['expanded_url']
                    if "?utm_campaign=twitter&utm_medium=twitter&utm_source=twitter" in tmplink:
                        tmplink=tmplink.replace("?utm_campaign=twitter&utm_medium=twitter&utm_source=twitter","")
                    elif "?utm_campaign=twitter&utm_medium=twitter&utm_source=twitte" in tmplink:
                        tmplink=tmplink.replace("?utm_campaign=twitter&utm_medium=twitter&utm_source=twitte","")
                    repostLink.append(tmplink)
                else:
                    tmplink=tweet.entities['urls'][0]['expanded_url']
                    if "?utm_campaign=twitter&utm_medium=twitter&utm_source=twitter" in tmplink:
                        tmplink=tmplink.replace("?utm_campaign=twitter&utm_medium=twitter&utm_source=twitter","")
                    elif "?utm_campaign=twitter&utm_medium=twitter&utm_source=twitte" in tmplink:
                        tmplink=tmplink.replace("?utm_campaign=twitter&utm_medium=twitter&utm_source=twitte","")
                    #print("tmplink",tmplink)
                    repostLink.append(tmplink)
                    repostText.append(tweet.full_text[:tweet.full_text.find('http')-1].lower().replace('&amp;','&').replace('’','\''))#.replace('—','-').replace('–','-')
        else:#リンクなし（画像はあるかも）
            if tweet.full_text[:2] == "RT":
                print("引用リツイート")
            else:
                if "https://t.co/" in tweet.full_text:#リンクなしの画像ツイート
                    print("リンクなしの画像ツイート",tweet.full_text[:tweet.full_text.find("https://t.co/")])
                    repostText.append(tweet.full_text[:tweet.full_text.find("https://t.co/")].lower().replace('&amp;','&').replace('’','\''))#.replace('—','-').replace('–','-'))
                else:
                    repostText.append(tweet.full_text.lower().replace('&amp;','&').replace('’','\''))
                    
    tweetsFromSS = tweepy.Cursor(t.user_timeline,id="swimswamnews",tweet_mode='extended',include_entities=True).items(100)
    quoteIds=[]
    print("\n@SwimSwamNews")
    for tw in tweetsFromSS:
        if len(tw.entities['urls'])>0:#リンクあり
            if hasattr(tw,"full_text"):
                if "https://twitter.com" in tw.entities['urls'][0]['expanded_url']:
                    quoteIds.append(tw.id)
                    print("引用リツイート, ",tw.full_text)
                elif tw.full_text[:2] == "RT":
                    print("リツイート（リンクあり）, ",tw.full_text)
                elif "http" in tw.full_text[:tw.full_text.find('http')-1]:#本文なしリンクのみ
                    onlyTxt.append(tw.full_text[:tw.full_text.find('http')-1])
                    onlyLink.append(tw.entities['urls'][0]['expanded_url'].replace("?utm_campaign=twitter&utm_medium=twitter&utm_source=twitter",""))
                    onlytxt.append(tw.full_text[:tw.full_text.find('http')-1])
                else:#本文もリンクもあり
                    onlyLink.append(tw.entities['urls'][0]['expanded_url'].replace("?utm_campaign=twitter&utm_medium=twitter&utm_source=twitter",""))
                    onlyTxt.append(tw.full_text[:tw.full_text.find('http')-1].replace('&amp;','&').replace('’','\''))
                    onlytxt.append(tw.full_text[:tw.full_text.find('http')-1].lower().replace('&amp;','&').replace('’','\''))
        else:#リンクなし（画像はあるかも）
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
    print("#############################")
    for i in range(len(onlyLink)):
        T=onlyTxt[i]
        txt=onlyTxt[i].lower()
        link=onlyLink[i]#スラッシュも含む
        if "ow.ly/" in link:                                                            
            link=requests.get(link).url
        print("now is ",i,T)
        print(onlytxt[i+1:].count(txt),repostText.count(txt))
        newTweetflag=False
        if "https://t.co/" in txt:
            print("画像系ツイート",T,txt,link)
            print("repostでツイートされているか",txt[:txt.find("https://t.co/")],repostText.count(txt[:txt.find("https://t.co/")]),link in repostText)
            if onlytxt[i+1:].count(txt[:txt.find("https://t.co/")])==0 and repostText.count(txt[:txt.find("https://t.co/")])==0 and repostText.count(link)==0:   
                print("(SwimSwamでのツイートの数,repostでの当該ツイートの数)",onlytxt[i+1:].count(txt[:txt.find("https://t.co/")]),repostText.count(link)) 
                newTweetflag=True
        else:
            if onlytxt[i+1:].count(txt)==0 and repostText.count(txt)==0:
                print(onlyLink[i+1:].count(link),repostLink.count(link),repostLink.count(link[:-1]))
                if onlyLink[i+1:].count(link)==0 and (repostLink.count(link)==0 and repostLink.count(link[:-1])==0):
                    newTweetflag=True
                else:
                    print("表記ゆれがあったらしいけど、リンクをたどったら同じです。") 
                    print(link,"\n") 
        if newTweetflag:
            print(T,"is new one !!!")
            if link=="nolink":
                t.update_status(status=T)
                print("Linkなしバージョン",T)
            else:
                gazou=""
                honbun=""
                request = requests.get(link, stream=True)
                if request.status_code == 200:
                    soup=BeautifulSoup(requests.get(link).content,"html.parser")
                if soup.select("div.site-wrapper > #featured > .post-welcome-thumbnail"):
                    if soup.select("div.site-wrapper > #featured > .post-welcome-thumbnail")[0]["href"]:
                        gazou=soup.select("div.site-wrapper > #featured > .post-welcome-thumbnail")[0]["href"]
                else:
                    if soup.select_one("div.site-wrapper > #featured > div#blur-bkg"):
                        if BeautifulSoup(str(soup.select_one("div.site-wrapper > #featured > div#blur-bkg")),features="lxml").find('div')['style']:
                            gazou=cssutils.parseStyle(BeautifulSoup(str(soup.select_one("div.site-wrapper > #featured > div#blur-bkg")),features="lxml").find('div')['style'])['background-image'].replace('url(', '').replace(')', '')
                if soup.select("div.site-wrapper > #main > #content > article"):
                    honbun=soup.select("div.site-wrapper > #main > #content > article")[0].get_text()
                    honbun=honbun[honbun.find(soup.select("div.site-wrapper > #main > #content > article > p")[0].text):]
                    print("honbun",honbun[:30])
                if "twitter.com" in link:
                    print("引用リツイートなのでツイートしません")
                    #print(T+'\n'+link)
                else:
                    print(T+'\n'+link)
                    if gazou:
                        if honbun:
                            tweet_format = T+"\n"+link+"\n\n"+"{}"
                            tweet_text_changed = change_tweet_len(tweet_format, target=honbun)
                            print(tweet_text_changed)
                            post1(tweet_text_changed,gazou)
                        else:
                            post1(T+'\n'+link,gazou)
                    else:
                        if honbun:
                            tweet_format = T+"\n"+link+"\n\n"+"{}"
                            tweet_text_changed = change_tweet_len(tweet_format, target=honbun)
                            print(tweet_text_changed)
                            t.update_status(status=tweet_text_changed)
                        else:
                            t.update_status(status=T+'\n'+link)
            time.sleep(1)
    print("Done")

if __name__=="__main__":
    main()
