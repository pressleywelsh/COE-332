import requests

def get_org(org_id:str): 
    r = requests.get(f"https://api.github.com/orgs/tacc/{org_id}")
    return r.json()

def get_members(org_id:str): 
    mem = requests.get(f"https://api.github.com/orgs/{org_id}:/members")
    return mem.json()

print(get_org("tacc"))
