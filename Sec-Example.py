from sec_api import QueryApi
sec_api_key = "3e8be8ed56ed523711d04851bddcb79c604b09ab360650bc5088731ce3d13de4"
queryApi = QueryApi(api_key=sec_api_key)

query = {
  "query": { "query_string": {
      "query": "ticker:TSLA\"10-Q\"" #  AND filedAt:{2020-01-01 TO 2020-12-31} AND formType:
    } },
  "from": "0",
  "size": "10",
  "sort": [{ "filedAt": { "order": "desc" } }]
}

sec_filings = queryApi.get_filings(query)
print(sec_filings)
