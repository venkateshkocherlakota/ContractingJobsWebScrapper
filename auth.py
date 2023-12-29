import os
import json

def get_auth():
    if os.path.isfile('auth.json') == False:
        print('Auth file does not exist. Quitting ...')
        quit()

    with open('auth.json', 'r') as file:
        ath = json.load(file)
        apiKey = ath['xapiKey']
        auth = ath['authorization']
        candidateId = ath['candidateId']
    return (apiKey, auth, candidateId)