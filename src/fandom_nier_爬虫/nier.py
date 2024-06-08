import requests
import pandas as pd
import lxml
from lxml import etree
from bs4 import BeautifulSoup

headers = {
    'cookie':'_b2=S66yy3ieQH.1667366474545; _au_1d=AU1D-0100-001667366533-TQIMQW9K-FU4W; fandom_global_id=60d07702-acf3-4e10-9d7f-04349551747b; au_id=AU1D-0100-001667366533-TQIMQW9K-FU4W; wikia_beacon_id=z351G1m8Po; wikia_session_id=Dk0yzF_j7_; optimizelyEndUserId=oeu1687922524652r0.5928652079138892; AMP_264a9266b5=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJjMjk1MGQ5Ny0xYWI3LTQyZjItYTI3MC0wNzE3M2M3MmVhNGYlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNjg5NTg0NjgwMzI2JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTY4OTU4NTQ3OTkyMyUyQyUyMmxhc3RFdmVudElkJTIyJTNBMCU3RA==; ag=1; _ce.s=v~d33abe28cea6902e5010804e998dfeb38718363a~vpv~6~v11.rlc~1667366550034~lcw~1689699230312~lcw~1690214229050; _pubcid=3becefb1-66f0-45dc-b033-ff640673bd97; tracking-opt-in-status=accepted; tracking-opt-in-version=7; addtl_consent=1~2822.3116; euconsent-v2=CP2kfsAP2kfsACNAHAENAdEsAP_gAH_gACiQI1tR_D7NbWFD8Xp1YPs0eY1Hx1DYYkQgAASBAmABQAKQIIwCgkEwJASABAACAAAAIAZBAAAECABUAUAAQAAAIAFAIEAAgQAKIABAgAMRIgBICAIAAIEAEAAIgABREgAB2AgIQMKECEwAhAAAAAAAIAAAAAAFAgEAAAAAYAIIAAAAAggAAAgAAAIAAGAAABCCNYAZgoREABQEhIRSBhFAgBEEYQEEAAAAAEgQIAAEAAECAMAhBBIABAgAAAAAAAACAAAQAACAAIRABAAUAAACAAAAAAAAAACAAAQAAAASAAAAAAAACAAAAAAAAAQAAAAYEIQAAAAAhAAAAAACAAAAAAAQAAAAAAAAAAAAAAAAAAAAIAAAAAAAACAAAAAAAAgAAAAA.YAAAAAAAAAAA; _au_last_seen_iab_tcf=1702194973280; __qca=P0-218442249-1702194972781; ac_cclang=; ac_user_id=aco6n7hbcii3kwc01d42cdcfa319d4bf058150e4348e3bffb468c49d6dee1eda362ce104ba6453a; sitenoticeHidden=0; _pbjs_userid_consent_data=6682686700907513; Geo={%22region%22:%22HB%22%2C%22city%22:%22chongyang%22%2C%22country_name%22:%22china%22%2C%22country%22:%22CN%22%2C%22continent%22:%22AS%22}; basset=; sessionId=e24f3ccd-b13f-481e-84ba-0efd4eab14b6; _gid=GA1.2.681574008.1702969377; fan_visited_wikis=22439,2294949,2294461,3020578,14764,98388,2737001; tracking_session_id=e24f3ccd-b13f-481e-84ba-0efd4eab14b6; connectId={"ttl":86400000,"lastUsed":1702969379870,"lastSynced":1702969379870}; cto_bundle=SCy-IV9NR1Rvazl4STB3TnhiUmZmYzl0NWF3U2p1bjRpRkJSJTJGUFZkQXNCdUs0NGVPSmlaTFBjZDR0ZTBqQkY4enoyU2hET2dwN2FVZWxlOUxUUnpUeEcxTTl3RzBxNDZSRGplNjFHbiUyRlc3OWVOQ0dQeUZYZktBNE5mJTJCTDQxcllwS2xxV3QxMDVXVlBWQ3dXQ3ZhVjc2NXhjWHclM0QlM0Q; _au_last_seen_pixels=eyJhcG4iOjE3MDI5NjkzNzgsInR0ZCI6MTcwMjk2OTM3OCwicHViIjoxNzAyOTY5Mzc4LCJhZHgiOjE3MDI5NjkzNzgsImFkbyI6MTcwMjk2OTM3OCwib3BlbngiOjE3MDI5NjkzNzgsImdvbyI6MTcwMjk2OTM3OCwibWVkaWFtYXRoIjoxNjY4NTg3NTYwLCJzb24iOjE3MDI5NjkzOTUsInVucnVseSI6MTcwMjk2OTM5NSwiX2ZhbmRvbS1jb20iOjE2Njg1ODc3MTcsInJ1YiI6MTcwMjk2OTM3OCwidGFwYWQiOjE3MDI5NjkzNzgsImNvbG9zc3VzIjoxNzAyOTY5Mzk1LCJhbW8iOjE3MDI5NjkzOTV9; csrf_token_7edb4307044064c5213d44940aa94f48ab88fe0b5ead052fbb75851a981aa6c4=xXAHXcyF9BJnCWRaEoEzxS7pYkMPt23be7qvFXMDQOE=; fandom_session=MTcwMjk2OTY2NnxqYV9OaFZiMHVnbi04N0VKSXdNVURhUUxhMzR3MmNRWUQxSzk2UC1ESTdsem5Rdkw4X1kxUkFWSnktdVQ4bDhwMHRMRWs0U0M2dFdLWkhwR0xBMU5ZeG56TjBId1dCRFBySDVPa1dJNmVick5QRnJDLURfVWtqeFJyNS1OWldxVVB0MEN6ZFo4T3c9PXxecdH_a67OJXTpQXFBqOzB7pd12xJP38OMl5RQVz_bqg==; __gads=ID=39e06d62d54de592:T=1702194974:RT=1702969872:S=ALNI_Maj3EAh_yaHnkNv2WdDBRqNYOYt6Q; __gpi=UID=00000ca8c630534f:T=1702194974:RT=1702969872:S=ALNI_MbAv2lfLC02LuCSTNoqJoIvX4Y6Og; nol_fpid=uspq5ilzhx2yu4mldwbtbk9xgn9wo1687922524|1687922524203|1702970063300|1702970063316; pvNumber=1; pvNumberGlobal=17; _ga_LVKNCJXRLW=GS1.1.1702969377.18.1.1702970240.0.0.0; AMP_MKTG_6765a55f49=JTdCJTIycmVmZXJyZXIlMjIlM0ElMjJodHRwcyUzQSUyRiUyRmNuLmJpbmcuY29tJTJGJTIyJTJDJTIycmVmZXJyaW5nX2RvbWFpbiUyMiUzQSUyMmNuLmJpbmcuY29tJTIyJTdE; pv_number_global=17; pv_number=1; _ga=GA1.2.167196962.1667366528; _gat=1; AMP_6765a55f49=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjI2NDcxMWY3ZS02M2RmLTQ1ZDYtODdkNS02ZTg0ZjkzYmY1MDIlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzAyOTY5Mzc3NDEyJTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTcwMjk3MDI5NTM4NiUyQyUyMmxhc3RFdmVudElkJTIyJTNBMjM1JTdE; _ga_LFNSP5H47X=GS1.1.1702969377.4.1.1702970309.0.0.0',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
}

def get(chara):
    url ='https://nier.fandom.com/wiki/'+chara
    resp = requests.get(url, headers = headers)
    html = etree.HTML(resp.text)
    filename = chara+'.md'
    filepath = 'D:\\blog\\source\\_posts\\' + filename
    body = """---
title: Nier:{Rion}
excerpt: Nier:Reincarnation中{Rion}的个人故事
author: icyyoung
date: {{ date }}
tags: story
categories: Nier
index_img: /img/blog_default_img.jpg
banner_img: /img/blog_default_img.jpg
---
"""
    body = body.format(Rion = chara)
    with open(filepath, 'w',encoding = 'utf-8') as f:
        f.write(body)
        f.write('# ' + chara)
        f.write('\n\n# Character Story')
        for i in range(2,6):
            get_character_story(html,i,f)
        f.write('# Dark Memories')
        for i in range(2,6):
            get_dark_memory(html,i,f,2)
        f.write('# Recollections of Dusk')
        for i in range(2, 6):
            get_dark_memory(html, i, f,3)
        f.write('# Hidden Stories')
        for i in range(2,12):
            get_dark_memory(html,i,f,4)



def get_character_story(html,i,f):
    f.write('\n## Story %s'%(i-1))
    content = html.xpath('//*[@id="mw-content-text"]/div/div[3]/div[%s]/p/text()'%i)
    format_content = '\n'.join(content)
    f.write(format_content)
    content2 = html.xpath('//*[@id="mw-content-text"]/div/div[3]/div[%s]/text()'%i)
    format_content2 = '\n'.join(content2)
    f.write(format_content2)
    f.write('\n\n\n')



def get_dark_memory(html,i,f,story_name):
    f.write('\n## Story %s' % (i - 1))
    content2 = html.xpath('//*[@id="mw-content-text"]/div/div[4]/div[%s]/div/div[%s]//text()' % (story_name,i))
    format_content2 = '\n'.join(content2)
    f.write(format_content2)
    f.write('\n\n\n')

# //*[@id="mw-content-text"]/div/div[3]/div[2]
# //*[@id="mw-content-text"]/div/div[4]/div[2]/div/div[2]
# //*[@id="mw-content-text"]/div/div[4]/div[3]/div/div[2]
# //*[@id="mw-content-text"]/div/div[4]/div[4]/div/div[6]

# def get_hidden_story(html,i,f):
#     f.write('\n## Story %s' % (i - 1))
#     # f.write('\nStory %s'%(i-1))
#     content = html.xpath('//*[@id="mw-content-text"]/div/div[4]/div[3]/div/div[%s]//text()'%i)
#     format_content = '\n'.join(content)
#     f.write(format_content)
#     f.write('\n\n\n')


# def get_recollection_of_dusk(html,i,f):
#     f.write('\n## Story %s' % (i - 1))
#     # f.write('\nStory %s'%(i-1))
#     content = html.xpath('//*[@id="mw-content-text"]/div/div[4]/div[3]/div/div[2]//text()'%i)
#     format_content = '\n'.join(content)
#     f.write(format_content)
#     f.write('\n\n\n')






print("输出人物名称：")
name = input()
get(name)