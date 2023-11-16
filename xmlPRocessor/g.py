import typesense
import openai
import sys
import json
import uuid
openai.api_key = ''
client = typesense.Client({
  'nodes': [{
    'host': '', # For Typesense Cloud use xxx.a1.typesense.net
    'port': '443',      # For Typesense Cloud use 443
    'protocol': 'https',   # For  Typesense Cloud use https
    'path': '/api'
  }],
  'api_key': '',
  'connection_timeout_seconds': 1800
})

evaluate = "You evaluate if the User Request can be fulfilled with any of the potential solutions provided by the user. If you find one or more to be adequate, answer with the exact number of that potential solution(s). If you find none adequate, reply with 0. Your reply must be a valid a valid JSON Array like [1, 3]."
evaluated = ''

system = "You are to respond strictly with a compact structured JSON containing WordPress Coding Standards compliant Object Oriented PHP code in MVP pattern. Ensure the code is secure, follows modern practices, and is functional. Provide a JSON array of objects. Each object should have keys 'filename', 'content', and 'purpose'. Do not include any additional text outside the JSON format."
user = 'Create a Plugin for WordPress that registers a new custom post type \"User\" and a custom field \"Location\" available on that post type.'
assistant = "[{\"file\":\"The generated filename\",\"content\":\"generated php code\",\"purpose\":\"Purpose of the file and code\"},{...}]"
task = input("What do you need? ")

def upsert(reply,project,thing='partial'):
    for entry in reply:
        document = {
        	'filename': entry['filename'],
        	'content': entry['content'],
        	'purpose': entry['purpose'],
            'project': project,
            'type': thing
    	}
        client.collections['code_base'].documents.create(document)
        
def get_gpt_response(messages):
    try:
        response = openai.ChatCompletion.create(
			model='gpt-4',
			messages=messages,
			temperature=0.2,
			max_tokens=1500,
			top_p=0.1,
			frequency_penalty=0,
			presence_penalty=0,
		)
        return response['choices'][0]['message']['content']

    except Exception as e:
        result, stop = "Request failed with an exception", {e}
        print( result, stop)
        return False

search_parameters = {
'q'                          : task,
'query_by'                   : 'purpose',
'prefix'                     : False,
'remote_embedding_timeout_ms': 5000,
'include_fields'             : 'purpose,project',
'filter_by'                  : 'type:=project',
}
print("Searching for similar projects...")
similars = client.collections['code_base'].documents.search(search_parameters)
if similars.get('found', 0) >= 1:
    print("Similar projects found. Evaluating their relevance...")
    # Extract the "purpose" values from each of the "hits"
    purposes = [hit['document']['purpose'] for hit in similars['hits']]
    project_ids = [hit['document']['project'] for hit in similars['hits']]
    #['This file is the main CSS file for the theme. It also contains the theme header comment, which is used by WordPress to display theme information in the admin area.', 'A Custom WordPress theme with Bootstrap 5 styling.']
    #['8dbb607c-b3b8-4d7f-8dc5-53134dd191db', '8dbb607c-b3b8-4d7f-8dc5-53134dd191db']
    # Join the values with a newline character and return
    solutions = ', '.join(f"{idx+1}) {purpose}" for idx, purpose in enumerate(purposes))
    #1) This file is used to enqueue the Bootstrap 5 CSS file and the theme's main CSS file., 2) A Custom WordPress theme with Bootstrap 5 styling.
    messages = [
		{"role": "system", "content": evaluate},
		{"role": "user", "content": f"I need {task}. These potential solutions have been suggested: {solutions}."}
	]
    evaluated = get_gpt_response(messages)
else:
    print("No similar projects found. Generating new project...")
    evaluated = 'none'

if evaluated == "none":
    print("The similar projects found are not relevant. Generating new project...")
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
        {"role": "assistant", "content": assistant},
        {"role": "user", "content": task},
	]
    reply = json.loads(get_gpt_response(messages))
    project_id = str(uuid.uuid4())
    print(reply)
    upsert([{'filename': '','content': '','purpose': task}],project_id,thing='project')
    upsert(reply,project_id)
    
else:
    #[1, 2]
    selected_purposes = [purposes[index - 1] for index in json.loads(evaluated)]
    pitch = '\n'.join([f"{idx+1}. {value}" for idx, value in enumerate(selected_purposes)])

    print(f"There are similar projects, that might fit your requirement \"{task}\". This is a short description of the projects found:\n{pitch}")
    user_decision = input("Do you want to build upon the existing project? (Either enter a number or no): ")
    if user_decision.isdigit():
        user_decision_int = int(user_decision) -1
        if user_decision_int < len(project_ids):  # Assuming project_ids is a list
            search_parameters = {
			'q'                          : project_ids[user_decision_int],
			'query_by'                   : 'project',
			'prefix'                     : False,
			'remote_embedding_timeout_ms': 5000,
			'include_fields'             : 'content,purpose,filename',
            'filter_by'                  : 'type:=partial',
			}
            baseproject = client.collections['code_base'].documents.search(search_parameters)
            print(json.dumps(baseproject, indent=4))
        else:
            print("Entered number is out of range.")
    else:
        print("Generating new project")
        messages = [
			{"role": "system", "content": system},
			{"role": "user", "content": user},
			{"role": "assistant", "content": assistant},
			{"role": "user", "content": task},
		]
        reply = json.loads(get_gpt_response(messages))
        project_id = str(uuid.uuid4())
        upsert([{'filename': '','content': '','purpose': task}],project_id,thing='project')
        upsert(reply,project_id)
        print("New Project Generated:")
        print(json.dumps(reply,indent=4))
        print(project_id)
				
schema = {
  "name": "code_base",
  "fields": [
    {
      "name" : "filename", 
      "type" : "string"
    },
	{
      "name" : "content",
      "type" : "string"
    },
	{
      "name" : "purpose",
      "type" : "string"
    },
    {
      "name" : "project",
      "type" : "auto"
    },
    {
      "name" : "thing",
      "type" : "auto"
    },
    {
      "name" : "embedding",
      "type" : "float[]",
      "embed": {
        "from": [
          "purpose"
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
# search_parameters = {
# 'q'                          : 'Create a Plugin for WordPress that registers a new custom post type \"User\" and a custom field \"Location\" available on that post type.',
# 'query_by'                   : 'embedding',
# 'prefix'                     : False,
# 'remote_embedding_timeout_ms': 5000,
# #'offset'                     : 1,
# 'per_page'                   : 3,
# }

# v_search_params = {
# 	'q'                          : '*',
# 	'prefix'                     : False,
# 	'remote_embedding_timeout_ms': 5000,
#     'vector_query': "embedding:([], id: 15463)"
# }
#print( client.collections['code_base'].documents.search(search_parameters) )
