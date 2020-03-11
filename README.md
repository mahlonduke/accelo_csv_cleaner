# accelo_company_name_adder

This app will take an export of data from Delighted (https://delighted.com/), and format it for importing into Accelo.  The import can be used to create just Companies and Contacts, or Companies, Contacts and Assets.  

Custom fields will need to be created in Accelo ahead of time to store nonstandard data such as "Score".

# Authentication
Authentication is performed using "Basic" authentication.  The Client ID and Secret used in that authentication are contained in a separate file titled api_config.py  
