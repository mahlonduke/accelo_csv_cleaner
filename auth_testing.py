# Import library dependencies
import pandas as pd
import numpy as np
import requests
import pprint as pp
import math
import re


# API Variables
deployment = 'markjellison'
token = 'e0lsIgICJ2rDoxzfFYGEJlgXiA~bfR9y'
clientId = 'b854b670e6@markjellison.accelo.com'
clientSecret = 'OtTIIXjbOZifR8TcLDm.2eKtnLXA7QFX'

# Query Defaults
email = 'customer.owner.affinitylive@gmail.com'
companyId= '2195'

# API Endpoint Setup
urlAffiliations = f'https://{deployment}.api.accelo.com/api/v0/affiliations?_fields=id,email,company&_search={email}&_limit=1'
urlCompanies = f'https://{deployment}.api.accelo.com/api/v0/companies?_filters=id({companyId})&_fields=name&_limit=1'

# API Header Setup
headers = {'Content-Type': 'application/json',
          'Authorization': f'Basic  {token}'}
