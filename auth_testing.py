# Import library dependencies
import pandas as pd
import numpy as np
import requests
import json
import pprint as pp
import math
import re
import base64

# API Variables
deployment = 'internal-zapier-testing'
clientId = 'da14af208e@internal-zapier-testing.accelo.com'
clientSecret = 'Sb7ejmW0UDF3hwUw6UiW0QuBuD7vqAxS'

# Query Defaults
email = 'customer.owner.affinitylive@gmail.com'
companyId= '2195'

# API Endpoint Setup
urlAffiliations = f'https://{deployment}.api.accelo.com/api/v0/affiliations?_fields=id,email,company&_search={email}&_limit=1'
urlCompanies = f'https://{deployment}.api.accelo.com/api/v0/companies?_filters=id({companyId})&_fields=name&_limit=1'

preCoding = f'{clientId}:{clientSecret}'
encoded = str(base64.b64encode(preCoding.encode("utf-8")), "utf-8")


urlAuthorize = f'https://{deployment}.api.accelo.com/oauth2/v0/token'

# API Header Setup
authHeaders = {'Authorization': f'Basic {encoded}',
          'Content-Type': 'application/json'}

# API Body Setup
body = {
    "grant_type": "client_credentials",
    "scope": "read(all)",
    "expires_in": "3600"
}

print("--------------------Debugging Details------------------------------")
print("Authentication:")
print(f'Client ID: {clientId}')
print(f'Client Secret: {clientSecret}')
print(f'Encoded ID:Secret: {encoded}\n\n')

print(f'Token Request Header: {authHeaders}')
print(f'Token Request Body: {body}\n\n')
response = requests.post(urlAuthorize, headers=authHeaders, data=json.dumps(body)).json()
token = response['access_token']
print(f'Access Token returned when supplying encoded ID & secret: {token}')
# API Header Setup Using new Token
headers = {'Content-Type': 'application/json',
          'Authorization': f'Bearer {token}'}
print(f'Request Header Using new Token: {headers}')
response = requests.get(urlAffiliations, headers=headers).json()
print(f'Response when making a request using the new token: {response}')
print("------------------End Debugging Details------------------------------")
