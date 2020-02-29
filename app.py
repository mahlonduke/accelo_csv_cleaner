# Import library dependencies
import pandas as pd
import numpy as np
import requests
import pprint as pp
import math
import re
import base64

# API Variables
deployment = 'markjellison'
token = 'e0lsIgICJ2rDoxzfFYGEJlgXiA~bfR9y'

# Query Defaults
email = 'customer.owner.affinitylive@gmail.com'
companyId= '2195'

# API Endpoint Setup
urlAffiliations = f'https://{deployment}.api.accelo.com/api/v0/affiliations?_fields=id,email,company&_search={email}&_limit=1'
urlCompanies = f'https://{deployment}.api.accelo.com/api/v0/companies?_filters=id({companyId})&_fields=name&_limit=1'

# API Header Setup
headers = {'Content-Type': 'application/json',
          'Authorization': f'Bearer {token}'}

# Open the source CSV
source = pd.read_csv('CSV Files/delighted-data_24-February-2020.csv')

# Create a new DF with just the relevant columns
data = source[['Name', 'Email', 'Score', 'Comment', 'Response Timestamp', 'access_level', 'company_id', 'company_name', 'Delighted Country', 'domain', 'industry_template', 'manager', 'monthly_spend']]

# Rename the columns
data = data.rename(columns={"access_level": "Access Level", "company_id": "Company ID", "company_name": "Company Name", "domain": "Domain", "industry_template": "Industry", "manager": "Manager", "monthly_spend": "MRR", "Name": "Original Name"})

# Replace any scores of 0 with "Zero"
data.loc[(data.Score == 0), 'Score']='Zero'

# Copy the contents of the Score column as "Title"
data['Title'] = data['Score']

# Loop through the data
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
                response = requests.get(urlAffiliations, headers=headers).json()
                if response['response'] != []:

                    companyId = response['response'][0]['company']
                    data.loc[(data['Company Name'] == companyName), 'Company ID']=companyId
            except requests.exceptions.RequestException as e:
                print(f'API Error: {e}')
    except:
        pass

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

# Output the result to CSV
data.to_csv('CSV Result/CLEANED.csv', index=False)
