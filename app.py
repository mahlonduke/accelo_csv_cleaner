# Import library dependencies
import pandas as pd
import numpy as np
import requests
import json
import pprint as pp
import math
import re
import base64

# Local file dependencies
import api_config

# API Variables
deployment = 'hq'
clientId = api_config.clientId
clientSecret = api_config.clientSecret

#Encode the Client ID and Secret
preCoding = f'{clientId}:{clientSecret}'
encoded = str(base64.b64encode(preCoding.encode("utf-8")), "utf-8")

# Query Defaults
email = 'email@domain.com'
companyId= '123'

# API Endpoint Setup
urlAffiliations = f'https://{deployment}.api.accelo.com/api/v0/affiliations?_fields=id,email,company&_search={email}&_limit=1'
urlCompanies = f'https://{deployment}.api.accelo.com/api/v0/companies?_filters=id({companyId})&_fields=name&_limit=1'
urlAuthorize = f'https://{deployment}.api.accelo.com/oauth2/v0/token'

# API Setup
authHeaders = {'Authorization': f'Basic {encoded}',
          'Content-Type': 'application/json'}
body = {
    "grant_type": "client_credentials",
    "scope": "read(all)",
    "expires_in": "3600"
}
response = requests.post(urlAuthorize, headers=authHeaders, data=json.dumps(body)).json()
token = response['access_token']
headers = {'Content-Type': 'application/json',
          'Authorization': f'Bearer {token}'}

# Open the source CSV
filenameSuccessful = 'no'
while filenameSuccessful == 'no':
    filename = input('Please enter the source filename (no file extension): ')
    try:
        source = pd.read_csv(f'{filename}.csv')
        print("File found.  Loading the file and cleaning its data now...")
        filenameSuccessful = 'yes'
    except:
        print("No such file found.\n\n")

# Create a new DF with just the relevant columns
data = source[['Name', 'Email', 'Score', 'Comment', 'Response Timestamp', 'access_level', 'company_id', 'company_name', 'Delighted Country', 'domain', 'industry_template', 'manager', 'monthly_spend']]

# Rename the columns
data = data.rename(columns={"access_level": "Access Level", "company_id": "Company ID", "company_name": "Company Name", "domain": "Domain", "industry_template": "Industry", "manager": "Manager", "monthly_spend": "MRR", "Name": "Original Name"})

# Replace any scores of 0 with "Zero"
data.loc[(data.Score == 0), 'Score']='Zero'
print("'0' scores successfully replaced with 'Zero'...")

# Copy the contents of the Score column as "Title"
data['Title'] = data['Score']
print("'Title' column successfully created...")

# Loop through the data
print(f'Checking for blank Company IDs...')
for index, row in data.iterrows():
    # Remove the timestamp from Response Timestamp
    companyName = row['Company Name']
    splitString = row['Response Timestamp'].split()
    data.loc[(data['Company Name'] == companyName), 'Response Timestamp']=splitString[0]

    # Identify any rows with no Company ID, pull it from Accelo, and add it to the DF
    try:
        if math.isnan(row['Company ID']):
            email = row['Email']
            urlAffiliations = f'https://{deployment}.api.accelo.com/api/v0/affiliations?_fields=id,email,company&_search={email}&_limit=1'
            try:
                print(f'Blank Company ID found at row #{index}.  Checking HQ for the correct ID based on {email}')
                response = requests.get(urlAffiliations, headers=headers).json()
                if response['response'] != []:

                    companyId = response['response'][0]['company']
                    data.loc[(data['Company Name'] == companyName), 'Company ID']=companyId
                    print(f'New Company ID added: {companyId}')
                else:
                    print(f'Email address not found in HQ.  This is a new contact.')
            except requests.exceptions.RequestException as e:
                print(f'API Error: {e}')
    except:
        pass
print("Missing Company IDs successfully added...")
print("Times successfully removed from Response Timestamp...")

# Clean up the respondents' names
names = data['Original Name'].tolist()
updatedNames = []
for name in range(0, len(names)):
    # Remove all the special characters
    document = re.sub(r'\W', ' ', str(names[name]))
    document = re.sub(r'\s+', ' ', document, flags=re.I)
    updatedNames.append(document)
updatedNames

# Split each word in the names field into separate columns
nameLength = []
name1 = []
name2 = []
name3 = []
name4 = []
name5 = []
for i in updatedNames:
    splitName = i.split()
    name1.append(splitName[0])
    try:
        name2.append(splitName[1])
    except:
        name2.append('')
    try:
        name3.append(splitName[2])
    except:
        name3.append('')
    try:
        name4.append(splitName[3])
    except:
        name4.append('')
    try:
        name5.append(splitName[4])
    except:
        name5.append('')
data['First Name'] = name1
data['Last Name'] = name2
data['Other Name 1'] = name3
data['Other Name 2'] = name4
data['Other Name 3'] = name5
print("Name successfully split into separate columns...")

# Output the result to CSV
cleanedFilename = filename + '-Cleaned.csv'
data.to_csv(cleanedFilename, index=False)
print(f'Cleanup complete.  Cleaned file is named {cleanedFilename}')
