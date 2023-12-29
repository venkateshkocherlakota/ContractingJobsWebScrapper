import csv
from api import already_applied, search_job_posts, is_c2c

def get_posts(search_param, api_auth_key):
    posts_raw = search_job_posts(search_param, api_auth_key)
    posts_data = extract_relevant_data(posts_raw)
    
    if len(posts_data) == 0:
        print('No Posts available. Try changing search param. Quitting ...')
        quit()

    return posts_data
    
def extract_relevant_data(data):
    extracted_data = []
    for item in data:
        entry = {
            'jobId': item.get('jobId', None),
            'title': item.get('title', None),
            'summary': item.get('summary', None),
            'postedDate': item.get('postedDate', None),
            'detailsPageUrl': item.get('detailsPageUrl', None),
            'jobLocation': item.get('jobLocation', None),
            'isC2C': True
        }
        extracted_data.append(entry)
    return extracted_data

def filter_c2c(posts):
    for item in posts:
        item['isC2C'] = is_c2c(item['detailsPageUrl'])

    c2c_posts = list(filter(lambda x : x['isC2C'] == True, posts))
    return c2c_posts

def remove_applied_posts(c2c_posts, auth, candidateId):
    new_posts = []
    
    for post in c2c_posts:
        if already_applied(post, auth, candidateId) == False:
            new_posts.append(post)
    
    if len(c2c_posts) == 0:
        print('No C2C positions available. Quitting ...')
        quit()

    return new_posts

def save_new_posts(new_posts):
    print('{} C2C positions available. Writing to "positions.csv"'.format(len(new_posts)))

    f = csv.writer(open("positions.csv", "w"))

    # Write CSV Header, If you dont need that, remove this line
    f.writerow(["jobId", "title", "summary", "postedDate", "detailsPageUrl", "jobLocation"])

    for post in new_posts:
        f.writerow([
            post["jobId"],
            post["title"],
            post["summary"],
            post["postedDate"],
            post["detailsPageUrl"],
            post["jobLocation"]
        ])
    