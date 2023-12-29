import requests

def search_job_posts(search_param, api_auth_key):
    url = 'https://job-search-api.svc.dhigroupinc.com/v1/dice/jobs/search?q=' + \
    search_param + \
    '&countryCode2=US&radius=3000&radiusUnit=mi&page=1&pageSize=1000&filters.employmentType=CONTRACTS%7CTHIRD_PARTY' + \
    '&filters.postedDate=ONE&fields=id%7CjobId%7Cguid%7Csummary%7Ctitle%7CpostedDate%7CmodifiedDate%7CjobLocation.displayName' + \
    '%7CdetailsPageUrl%7Csalary%7CclientBrandId%7CcompanyPageUrl%7CcompanyLogoUrl%7CpositionId%7CcompanyName%7CemploymentType' + \
    '%7CisHighlighted%7Cscore%7CeasyApply%7CemployerType%7CworkFromHomeAvailability%7CisRemote%7Cdebug&culture=en&includeRemote=true'
    
    response = requests.get(url, headers={"X-Api-Key": api_auth_key})
    
    if response.status_code != 200:
        print('Did not receive valid response. Quiting ...')
        quit()
    return response.json()['data']

def already_applied(position, auth, candidateId):
    response = requests.post(
        'https://api.prod.jobapplication-prod.dhiaws.com/graphql',
        data='{ "query":"query candidateAppliedToJob($jobId: ID!, $candidateId: ID!) { candidateAppliedToJob(jobId: $jobId, candidateId: $candidateId)'
        + ' { applied, applied_date }}","variables":{"jobId":"'
        + position['jobId'] +'","candidateId":"'+ candidateId +'"}}',
        headers={
            'Authorization': auth,
            'Content-Type': 'application/json'
        }
    )
    print(response.json())
    return response.json()['data']['candidateAppliedToJob']['applied']

def is_c2c(url):
    rsp = requests.get(url)
    txt = rsp.text.lower()
    if 'c2c' in txt or 'accepts corp to corp applications' in txt:
        return True
    return False