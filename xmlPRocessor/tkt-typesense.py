import typesense

client = typesense.Client({
  'nodes': [{
    'host': '', # For Typesense Cloud use xxx.a1.typesense.net
    'port': '8108',      # For Typesense Cloud use 443
    'protocol': 'http'   # For Typesense Cloud use https
  }],
  'api_key': '',
  'connection_timeout_seconds': 1800
})

# schema = {
#   "name": "wp_doc",
#   "enable_nested_fields": True,
#   "fields": [
#     {
#       "name" : "name", 
#       "type" : "auto"
#     },
# 	{
#       "name" : "type",
#       "type" : "auto"
#     },
# 	{
#       "name" : "arguments",
#       "type" : "auto"
#     },
# 	{
#       "name" : "descriptions",
#       "type" : "string[]"
#     },
# 	{
#       "name" : "tags",
#       "type" : "auto"
#     },
#     {
#       "name" : "embedding",
#       "type" : "float[]",
#       "embed": {
#         "from": [
#           "descriptions"
#         ],
#         "model_config": {
#           "model_name": "openai/text-embedding-ada-002",
#           "api_key": ""
#         }
#       }
#     }
#   ]
# }
schema = {
  "name": "dreams",
  "fields": [
    {
      "name" : "text", 
      "type" : "string"
    },
	{
      "name" : "date",
      "type" : "auto"
    },
	{
      "name" : "h_date",
      "type" : "auto"
    },
    {
      "name" : "embedding",
      "type" : "float[]",
      "embed": {
        "from": [
          "text"
        ],
        "model_config": {
          "model_name": "openai/text-embedding-ada-002",
          "api_key": ""
        }
      }
    }
  ]
}

#print(client.collections.create(schema))
#print( client.collections.retrieve() )
#print(client.collections['wordpress_doc'].retrieve())
#print(client.collections['wordpress_doc'].documents.export())
#print( client.collections['dreams'].delete() )
# with open('dreams-processed.jsonl') as jsonl_file:
#   print(client.collections['dreams'].documents.import_(jsonl_file.read().encode('utf-8'), {'batch_size': 100}))
search_parameters = {
'q'                          : 'What is QC',
'query_by'                   : 'embedding',
'prefix'                     : False,
'remote_embedding_timeout_ms': 5000,
#'offset'                     : 1,
'per_page'                   : 3,
}

v_search_params = {
	'q'                          : '*',
	'prefix'                     : False,
	'remote_embedding_timeout_ms': 5000,
    'vector_query': "embedding:([], id: 15463)"
}
print( client.collections['tukutoi_posts'].documents.search(v_search_params) )
