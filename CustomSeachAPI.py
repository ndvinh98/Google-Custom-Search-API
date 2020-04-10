#Requirements pip install --upgrade google-api-python-client
#if you get an error when installing google-api-python-client, you should unistall your pip then run 'python get-pip.py'
from googleapiclient.discovery import build
from multiprocessing import Pool
import time


query = "Thủ đô của Việt Nam là gì?" 
#change your key https://developers.google.com/custom-search/v1/overview, note that it provides 100 search queries per day for free
Seach_api_key ="AIzaSyBy-PVoHZdYRDU70gsLD-ALy5JabcZUICk" 

#change your custom search engine https://cse.google.com/cse/all
Custom_Search_Engine_ID ="013964321510468908374:fcs9cr0koid" 

start = time.time()
service = build("customsearch", "v1",developerKey=Seach_api_key)

def ggsearch(i):
    if (i == 0):
        res = service.cse().list(q=query,cx = Custom_Search_Engine_ID).execute()
    else:
        res = service.cse().list(q=query,cx = Custom_Search_Engine_ID,num=10,start = i*10).execute()
    return res['items']



if __name__ == '__main__':
    #multi processing
    pool = Pool(4)
    pages_content = pool.map(ggsearch,range(1))
    pool.terminate()

    #extract url, title
    pages_content = [j for i in pages_content for j in i]

    document_urls = []
    document_titles = []
    for page in pages_content:
        if 'fileFormat' in page:
            print('Skip ' +  page['link'])
            continue
        document_urls.append(page['link'])
        document_titles.append(page['title'])
        
    for i in range(0,10):
        print(document_titles[i])
        print(document_urls[i])

    print('Number of result: '+str(len(document_titles)))
    print('Time execute: '+str(time.time() - start))