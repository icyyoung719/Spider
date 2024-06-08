import requests
import pandas as pd
import html2text
from lxml import html
from lxml import etree
from bs4 import BeautifulSoup

headers = {
    'cookie':'testcookie=supportcheck; _b2=S66yy3ieQH.1667366474545; _au_1d=AU1D-0100-001667366533-TQIMQW9K-FU4W; fandom_global_id=60d07702-acf3-4e10-9d7f-04349551747b; wikia_beacon_id=z351G1m8Po; wikia_session_id=Dk0yzF_j7_; optimizelyEndUserId=oeu1687922524652r0.5928652079138892; AMP_264a9266b5=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJjMjk1MGQ5Ny0xYWI3LTQyZjItYTI3MC0wNzE3M2M3MmVhNGYlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNjg5NTg0NjgwMzI2JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTY4OTU4NTQ3OTkyMyUyQyUyMmxhc3RFdmVudElkJTIyJTNBMCU3RA==; ag=1; _pubcid=3becefb1-66f0-45dc-b033-ff640673bd97; tracking-opt-in-status=accepted; tracking-opt-in-version=7; addtl_consent=1~2822.3116; euconsent-v2=CP2kfsAP2kfsACNAHAENAdEsAP_gAH_gACiQI1tR_D7NbWFD8Xp1YPs0eY1Hx1DYYkQgAASBAmABQAKQIIwCgkEwJASABAACAAAAIAZBAAAECABUAUAAQAAAIAFAIEAAgQAKIABAgAMRIgBICAIAAIEAEAAIgABREgAB2AgIQMKECEwAhAAAAAAAIAAAAAAFAgEAAAAAYAIIAAAAAggAAAgAAAIAAGAAABCCNYAZgoREABQEhIRSBhFAgBEEYQEEAAAAAEgQIAAEAAECAMAhBBIABAgAAAAAAAACAAAQAACAAIRABAAUAAACAAAAAAAAAACAAAQAAAASAAAAAAAACAAAAAAAAAQAAAAYEIQAAAAAhAAAAAACAAAAAAAQAAAAAAAAAAAAAAAAAAAAIAAAAAAAACAAAAAAAAgAAAAA.YAAAAAAAAAAA; __qca=P0-218442249-1702194972781; csrf_token_7edb4307044064c5213d44940aa94f48ab88fe0b5ead052fbb75851a981aa6c4=xXAHXcyF9BJnCWRaEoEzxS7pYkMPt23be7qvFXMDQOE=; fandom_session=MTcwMjk2OTY2NnxqYV9OaFZiMHVnbi04N0VKSXdNVURhUUxhMzR3MmNRWUQxSzk2UC1ESTdsem5Rdkw4X1kxUkFWSnktdVQ4bDhwMHRMRWs0U0M2dFdLWkhwR0xBMU5ZeG56TjBId1dCRFBySDVPa1dJNmVick5QRnJDLURfVWtqeFJyNS1OWldxVVB0MEN6ZFo4T3c9PXxecdH_a67OJXTpQXFBqOzB7pd12xJP38OMl5RQVz_bqg==; _au_last_seen_iab_tcf=1707812250214; basset=icFeaturedVideoPlayer-0_A_90:false|icFeaturedVideoPlayer-1_A_90:false|icConnatixPlayer-0_A_75:false; _pubcid_cst=HCw%2BLKMsPg%3D%3D; _gid=GA1.2.1017987844.1709976860; _scor_uid=0c8fa10cdcfe4b34a0350e5f8d47b839; Geo={%22region%22:%22HB%22%2C%22city%22:%22baoli%22%2C%22country_name%22:%22china%22%2C%22country%22:%22CN%22%2C%22continent%22:%22AS%22}; sessionId=e0d15b25-cde6-4c06-a2fe-355ade80c3d4; tracking_session_id=e0d15b25-cde6-4c06-a2fe-355ade80c3d4; __gads=ID=39e06d62d54de592:T=1702194974:RT=1710044265:S=ALNI_Maj3EAh_yaHnkNv2WdDBRqNYOYt6Q; __gpi=UID=00000ca8c630534f:T=1702194974:RT=1710044265:S=ALNI_MbAv2lfLC02LuCSTNoqJoIvX4Y6Og; __eoi=ID=fce1aabd5c5e190f:T=1709789419:RT=1710044265:S=AA-AfjY53S85peXt_4GoVotznplk; _ce.irv=returning; cebs=1; connectId={"ttl":86400000,"lastUsed":1710044358790,"lastSynced":1710044358790}; _ce.clock_event=1; _ce.clock_data=47%2C115.156.140.188%2C1%2Cd94a27a56e6a143d4c900b9014d6ba5d; cebsp_=1; _ce.s=v~d33abe28cea6902e5010804e998dfeb38718363a~vpv~8~v11.rlc~1667366550034~lcw~1710044362813~lva~1710044358540~v11.fhb~1710044359179~v11.lhb~1710044359179~v11.cs~362001~v11.s~5d4c29f0-de95-11ee-a8cc-8391152a4383~v11.sla~1710044363276~gtrk.la~ltl09f0b~v11.send~1710044362813~lcw~1710044363277; fan_visited_wikis=22439,2294949,2294461,3020578,14764,98388,2737001,689899,57800,177; nol_fpid=ibs8oudxj4sz4zx2mfpchjnacujxm1704597107|1704597107771|1710044454072|1710044454080; cto_bundle=UF7YSV9qNXl0WHklMkZMQ2E4TUYwMm1UTktsSHJzMTFyUDNycHJZbSUyRmtwYXNvdExmNEFSSThiTlNaMXlkTU5XUnBXVHZPUHE2aUlmeExabXdVS1NUMyUyRklWVE0ySmlYN25oNjZzVlhkaFJjTnIzNWwzJTJGd3ZHcEc1RVExRFdrUWtxTzN4U0ZtandwSXl5V2ZScGVJdzElMkYlMkIyR01HMlElM0QlM0Q; FCNEC=%5B%5B%22AKsRol-CpEI7Gt2lWwhAXmlaxNjXCUer6uKTbuaJ0E-GHEQWGJP2DG6PTtygVKQDjHZHGn1BNrxlwrGODJGMZ8jFl5RA67DeBjVSROTkTh1WM2y0cInfR9gFW8038iNUVJAbFgc7IaFbYCYCQM09M7vBqwIsOSOUIQ%3D%3D%22%5D%5D; _ga_FVWZ0RM4DH=GS1.1.1710044278.11.1.1710044543.8.0.0; pvNumber=7; pvNumberGlobal=16; _gat=1; pv_number_global=16; pv_number=7; AMP_MKTG_6765a55f49=JTdCJTdE; AMP_6765a55f49=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjI2NDcxMWY3ZS02M2RmLTQ1ZDYtODdkNS02ZTg0ZjkzYmY1MDIlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzEwMDQ0MjY0NDYwJTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTcxMDA0NTM0MTg2NiUyQyUyMmxhc3RFdmVudElkJTIyJTNBMTU4MCU3RA==; _ga_LVKNCJXRLW=GS1.1.1710044265.52.1.1710045342.0.0.0; _ga=GA1.1.167196962.1667366528; _ga_LFNSP5H47X=GS1.1.1710044265.32.1.1710045347.0.0.0',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
}

def get(chara):
    url ='https://drakengard.fandom.com/wiki/'+chara+'/Novella'
    resp = requests.get(url, headers = headers)
    html = etree.HTML(resp.text)
    filename = chara+'.md'
    filepath = 'D:\\blog\\source\\_posts\\' + filename
    body = """---
title: Darkengard 3:{Rion}
excerpt: Darkengard 3中{Rion}的个人故事
author: icyyoung
date: {{ date }}
tags: novella
categories: Darkengard
index_img: /img/drakengard/zero.webp
banner_img: /img/blog_default_img.jpg
---
"""
    body = body.format(Rion = chara)
    with open(filepath, 'w', encoding = 'utf-8') as f:
        f.write(body)
        f.write('# ' + chara)
        f.write('\n\n# Character Story\n\n')
        for img in html.xpath('//img'):
            img.getparent().remove(img)
        content = html.xpath('//*[@id="mw-content-text"]/div')[0]
        content_str = etree.tostring(content, encoding = 'unicode')
        f.write(content_str)


#//*[@id="mw-content-text"]/div
#//*[@id="mw-content-text"]/div
print("输出人物名称：")
name = input()
get(name)