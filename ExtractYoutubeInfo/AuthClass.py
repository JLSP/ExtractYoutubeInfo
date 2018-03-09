from google_auth_oauthlib import flow

class AuthClass(object):

    def __init__(self, clientsecret):
        """Return a Customer object whose name is *name*.""" 
        self.clientsecret = clientsecret
        self.appflow = None

    def set_auth_bigquery(self,launch_browser=True):
            appflow = flow.InstalledAppFlow.from_client_secrets_file(
                self.clientsecret,
                scopes=['https://www.googleapis.com/auth/bigquery'])
            
            if launch_browser:
                appflow.run_local_server()
            else:
                appflow.run_console()
            
            self.appflow = appflow

    def get_auth_bigquery(self):
            return self.appflow

    auth = property(get_auth_bigquery,set_auth_bigquery)


