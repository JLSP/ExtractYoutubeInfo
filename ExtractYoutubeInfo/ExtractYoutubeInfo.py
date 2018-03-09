# Sample Python code for user authorization

import os
import json
import google.oauth2.credentials

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)


def youtube_search(service, q, max_results=50,order="relevance", token=None, location=None, location_radius=None):



    search_response = service.search().list(

    q=q,

    type="video",

    pageToken=token,

    order = order,

    part="id,snippet", # Part signifies the different types of data you want 

    maxResults=max_results,

    location=location,

    locationRadius=location_radius).execute()

    #with open('testfile.txt', 'w', encoding='utf8') as outfile:
    #        json.dump(search_response, outfile, ensure_ascii=False)

    part = ['snippet','statistics','contentDetails','topicDetails','recordingDetails']
    youtube_dict={"items":[]}

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            video_dict ={
                            "videoid":search_result['id']['videoId']
                        }
            for partname in part:
                response_stat=get_videopart(service,partname,search_result['id']['videoId'])
                video_dict[partname]=response_stat
                
            youtube_dict["items"].append(video_dict)

            #input("Press Enter to continue...")
    with open('testfile.txt', 'w', encoding='utf8') as outfile:
        json.dump(youtube_dict, outfile)      

def get_videopart(service,partname,videoid):
   try: 
    response = service.videos().list(
                part=partname,
                id=videoid).execute()
    
    response_stat=response['items'][0][partname]
    return response_stat
   except Exception as inst:
                print(type(inst))
                print(inst.args)
                print(inst)  

if __name__ == '__main__':
  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
  service = get_authenticated_service()
  youtube_search(service,'UFO')

