import requests
import os
import sys
 
## Token(bearer_all_vaults_token) for listing all the existing vaults.
data = {
'grant_type': 'client_credentials',
'client_id': 'a4735b5a-a10d-441a-8ea5-74a9d747d510',
'client_secret': '@7F:X-:9ldp6bT7kVHH7dVs4LScG69a/',
'resource': 'https://management.azure.com/'
}
all_vaults = requests.post('https://login.microsoftonline.com/06408ebc-5eb8-4b0d-827f-76dd3b58bc84/oauth2/token', data=data)
all_vaults_token = all_vaults.json()
bearer_all_vaults_token = all_vaults_token["access_token"]
#print("token %s" %bearer_all_vaults_token)
#print("==================================================")
 
## Token(bearer_individual_vault_info_token) for processing the vaults.
data = {
 'grant_type': 'client_credentials',
 'client_id': 'a4735b5a-a10d-441a-8ea5-74a9d747d510',
'client_secret': '@7F:X-:9ldp6bT7kVHH7dVs4LScG69a/',
 'resource': 'https://vault.azure.net\n'
}
vault_info = requests.post('https://login.microsoftonline.com/06408ebc-5eb8-4b0d-827f-76dd3b58bc84/oauth2/token', data=data)
individual_vault_info = vault_info.json()
bearer_individual_vault_info_token = individual_vault_info["access_token"]
#print("token : %s" %bearer_individual_vault_info_token)
#print("==================================================")
 
## Using bearer_all_vaults_token list the existing vault names.
headers = {
 'Authorization': 'Bearer %s' %bearer_all_vaults_token,
}
params = (
 ('api-version', '2015-06-01'),
)
vaults = requests.get('https://management.azure.com/subscriptions/168914c8-0d14-44cc-b8c3-0690d653fd17/resourceGroups/testingkey-rg/providers/Microsoft.KeyVault/vaults', headers=headers, params=params)
vault_name = vaults.json()
p = vault_name["value"] ## "P" will hold the entire valut JSON as a LIST
lst=[]
lst_vault=[]
## Iterating "P" and extracting the vault name "val"
for i in range(len(p)):
    val = p[i]["id"].split("/")[-1]
    #print("Secrets extracting from %s vault" %val)
    headers = {
        'Authorization': 'Bearer %s' %bearer_individual_vault_info_token,
        'Content-Type': 'application/json',
        }
    params = (
        ('api-version', '2016-10-01'),
        )
    response3 = requests.get('https://%s.vault.azure.net/secrets'% val, headers=headers, params=params)
    resp3 = response3.json()
    x3 = resp3["value"]
    for k in range(len(x3)):
        id1 = x3[k]["id"]
        id2 = x3[k]["id"].split("/")[-1]
        headers = {
            'Authorization': 'Bearer %s' %bearer_individual_vault_info_token,
            'Content-Type': 'application/json',
            }
        params = (
            ('api-version', '2016-10-01'),
        )
        response4 = requests.get('%s' %id1, headers=headers, params=params)
        x4 = response4.json()
        val5 = x4["value"]
        con = "%s__%s"%(val,id2)
        lst.append(val5)
        lst_vault.append(con)
key_value = dict(zip(lst_vault,lst))
final_secret_value = key_value[str(sys.argv[1])]
print(final_secret_value)
