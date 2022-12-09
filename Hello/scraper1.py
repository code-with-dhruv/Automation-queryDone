from __future__ import print_function
import time
import pandas as pd
import woslite_client
from woslite_client.rest import ApiException
from pprint import pprint


a=(input("Enter Query"))
# Configure API key authorization: key
configuration = woslite_client.Configuration()
configuration.api_key['X-ApiKey'] = 'e9bc939b6ec9edb8c7cb88f03da101f88bdb4942'

# create an instance of the API class
integration_api_instance = woslite_client.IntegrationApi(
    woslite_client.ApiClient(configuration))
search_api_instance = woslite_client.SearchApi(
    woslite_client.ApiClient(configuration))
# str | Database to search. Must be a valid database ID, one of the following: BCI/BIOABS/BIOSIS/CCC/DCI/DIIDW/MEDLINE/WOK/WOS/ZOOREC. WOK represents all databases.
database_id = 'WOS'
# unique_id = 'WOS:000270372400005'  # str | Primary item(s) id to be searched, ex: WOS:000270372400005. Cannot be null or an empty string. Multiple values are separated by comma.
# str | User query for requesting data, ex: TS=(cadmium). The query parser will return errors for invalid queries.
usr_query = 'AU={}'.format(a)
count = 100  # int | Number of records returned in the request
# int | Specific record, if any within the result set to return. Cannot be less than 1 and greater than 100000.
first_record = 1
# str | Language of search. This element can take only one value: en for English. If no language is specified, English is passed by default. (optional)
lang = 'en'
# str | Order by field(s). Field name and order by clause separated by '+', use A for ASC and D for DESC, ex: PY+D. Multiple values are separated by comma. (optional)
sort_field = 'PY+D'

api_response = search_api_instance.root_get(database_id, usr_query, count, first_record, lang=lang,
                                            sort_field=sort_field)
output = []
for i in range(1, 100):
    title = api_response.data[i].title.title[0]
    for j in range(1, len(api_response.data[i].author.authors)):
        author = api_response.data[i].author.authors[j]
    ut = api_response.data[i].ut

    line = {'Title': title, 'authors': author, 'id': ut}
    output.append(line)
df = pd.DataFrame(output)
df.to_csv('output.csv')

print("Completed")

