from pyecore.resources import ResourceSet, URI
from pyecore.ecore import EClass
import sys

import openai
import time 
openai.api_key = "sk....hr060"#Fill the API key
model_engine = "gpt-3.5-turbo" 

start = time.time()
rset = ResourceSet()
resource = rset.get_resource(URI('sclang.ecore'))
mm_root = resource.contents[0]
rset.metamodel_registry[mm_root.nsURI] = mm_root
resource = rset.get_resource(URI('V2.sclang'))#Grading_System.sclang or V2.sclang
model_root = resource.contents[0]

# print(model_root.scontract[0].targetPlatform)
the_contract = model_root.scontract[0]
elements = the_contract.element
participants = []
assets = []
transactions = []

for e in elements:
    # print(e.__class__.__name__)
    if e.__class__.__name__== 'Participant':
        participants.append(e)
    elif e.__class__.__name__== 'Asset':
        assets.append(e)
    elif e.__class__.__name__== 'Transaction':
        transactions.append(e)

parameters = []
for a in assets:
    for p in a.element:
        if p.__class__.__name__== 'Parameter':
            parameters.append(p)

participant_names =[]
for p in participants:
    participant_names.append(p.name)   

parameter_names =[]
for p in parameters:
    parameter_names.append(p.name)  

transaction_names =[]
for t in transactions:
    transaction_names.append(t.name)        

prompt = 'There are %d participants'%(len(participants))+' in the contract.'
prompt = prompt  + ' The participants are: '+ " and ".join(participant_names)+'.'
prompt = prompt  + ' There are %d parameters.'%(len(parameters))
prompt = prompt  +' The parameters are: '+ " and ".join(parameter_names)+'.'
prompt = prompt  +' There are %d transactions.'%(len(transactions))
prompt = prompt  + ' The transactions are: '+ " and ".join(transaction_names)+'.'
    
for p in participants:
    prompt = prompt + ' Participant '+p.name+' can execute transaction '+ p.relationship[0].to.name+'.'

prompt = prompt + ' Write the scenario in Solidity version 0.6.'
end  = time.time()

print(prompt)
print(end - start)

#sys.exit(0)
start = time.time()

response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
       
        {"role": "user", "content": prompt}
    ])

message = response.choices[0]['message']
print("{}:\n {}".format(message['role'], message['content']))
end  = time.time()
print(end - start)