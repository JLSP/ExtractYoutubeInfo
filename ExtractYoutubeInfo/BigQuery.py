from google.cloud import bigquery
import os
import json
from google_auth_oauthlib import flow
from AuthClass import AuthClass

#def authenticate(launch_browser=True):
#    
#
#    appflow = flow.InstalledAppFlow.from_client_secrets_file(
#        'client_secret.json',
#        scopes=['https://www.googleapis.com/auth/bigquery'])
#
#    if launch_browser:
#        appflow.run_local_server()
#    else:
#        appflow.run_console()
#
#    project=appflow.client_config["project_id"]
#    client = bigquery.Client(project=project,credentials=appflow.credentials)
#
#    return client
 
def run_query(credentials, project, query):
    
    client = bigquery.Client(project=project, credentials=credentials)
    query_job = client.query(query)

    # Print the results.
    for row in query_job.result():  # Wait for the job to complete.
        print(row)

if __name__ == '__main__':
  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

  #client = authenticate_and_query(launch_browser=True)
  #result=run_query(appflow.credentials, project, query)
  authToken = AuthClass("client_secret.json")
  authToken.set_auth_bigquery()

  project= authToken.appflow.client_config["project_id"]

  client = bigquery.Client(project=project,credentials=authToken.appflow.credentials)
  job_config = bigquery.QueryJobConfig()
  job_config.use_legacy_sql = False

  query_job = client.query("""
        SELECT
          date,
          id,
          statename,
          MAX(prcp) AS prcp,
          MAX(tmin) AS tmin,
          MAX(tmax) AS tmax
        FROM (
          SELECT
            wx.id,
            wx.date AS date,
            b.name AS stateName,
            IF (wx.element = 'PRCP', wx.value/10, NULL) AS prcp,
            IF (wx.element = 'TMIN', wx.value/10, NULL) AS tmin,
            IF (wx.element = 'TMAX', wx.value/10, NULL) AS tmax
          FROM
            `bigquery-public-data.ghcn_d.ghcnd_2018` AS wx
          INNER JOIN `bigquery-public-data.ghcn_d.ghcnd_stations` as a
          ON wx.id=a.id
          INNER JOIN `bigquery-public-data.ghcn_d.ghcnd_states` as b
          ON a.state=b.code
          WHERE DATE_DIFF(CURRENT_DATE(), wx.date, DAY) < 3

        )
        GROUP BY
         date,id,statename""", job_config=job_config)
  
  result ={"rows":[]}
  for row in query_job.result():
        rowDict = {
                    "date":row[0],
                    "id":row[1],
                    "statename":row[2],
                    "precip":row[3],
                    "tmin":row[4],
                    "tmax":row[5]
                  }
        result["rows"].append(rowDict)

  with open('testfileWeather.txt', 'w', encoding='utf8') as outfile:
        json.dump(result, outfile, default=str)
