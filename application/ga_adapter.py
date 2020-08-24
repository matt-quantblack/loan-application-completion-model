
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

class GAAdapter:

    def __init__(self):

        self.service = None

    def connect(self, scopes, key_file_location, api_name='analytics', api_version='v3'):
        """Connects a service that communicates to a Google API.

            Args:
                api_name: The name of the api to connect to.
                api_version: The api version to connect to.
                scopes: A list auth scopes to authorize for the application.
                key_file_location: The path to a valid service account JSON key file.
            """

        # Get the credentials from local storage
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            key_file_location, scopes=scopes)

        # Build the service object.
        self.service = build(api_name, api_version, credentials=credentials)

    def __get_account_by_index(self, index):

        # Get a list of all Google Analytics accounts for this user
        accounts = self.service.management().accounts().list().execute()

        # Get the Google Analytics account by index.
        if accounts.get('items'):
            account = accounts.get('items')[index].get('id')
            return account
        else:
            return None

    def __get_property_by_index(self, account, index):

        # Get a list of all the properties for the first account.
        properties = self.service.management().webproperties().list(
            accountId=account).execute()

        # Get the Google Analytics property by index.
        if properties.get('items'):
            prop = properties.get('items')[index].get('id')
            return prop
        else:
            return None



    def get_profiles(self, account=None):
        """ Get's the available Google Analytics profile names and ids

            Args:
                account: A google analytics account object
        """

        #make sure a connection has been made
        if self.service is None:
            raise TypeError("A Google Analytics Service object has not been created. Run connect() first.")

        #get the first available account if no account is passed
        if account is None:
            account = self.__get_account_by_index(0)

        #make sure wer have an account either passed in or default account
        if account is not None:
            prop = self.__get_property_by_index(account, 0)

            # Get a list of all views (profiles) for the first property.
            profiles = self.service.management().profiles().list(
                accountId=account,
                webPropertyId=prop).execute()

            # Build a simple list of id and name for each profile
            if profiles.get('items'):

                profile_list = []

                for p in profiles.get('items'):
                    profile_list.append({'id': p.get('id'), 'name': p.get('name')})

                return profile_list

        # Return None if not successful
        return None

    def get_data(self, profile_id, dimensions, start_date='7daysAgo'):
        """ Get's the a generic data snapshot associated with the profile id

                Args:
                    profile_id: The profile id for the Google Analytics profile
            """

        # make sure a connection has been made
        if self.service is None:
            raise TypeError("A Google Analytics Service object has not been created. Run connect() first.")

        results = self.service.data().ga().get(
            ids='ga:' + profile_id,
            start_date=start_date,
            end_date='today',
            dimensions=dimensions,
            metrics='ga:users'
        ).execute()

        return results


def get_profiles(key_file_location):
    ga_adapter = GAAdapter()
    ga_adapter.connect(scopes=['https://www.googleapis.com/auth/analytics.readonly'],
                       key_file_location=key_file_location)
    profiles = ga_adapter.get_profiles()

    return profiles


def get_data(key_file_location, profile_id, dimensions, start_date):
    ga_adapter = GAAdapter()
    ga_adapter.connect(scopes=['https://www.googleapis.com/auth/analytics.readonly'],
                       key_file_location=key_file_location)
    df = ga_adapter.get_data(profile_id, dimensions, start_date)

    return df
