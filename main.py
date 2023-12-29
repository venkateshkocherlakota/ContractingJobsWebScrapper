# python imports
import sys
# custom imports
from auth import get_auth
from lib import get_posts, filter_c2c, remove_applied_posts, save_new_posts

# retrieve auth data
auth = get_auth()
print('Candidate auth data fetched.')
# retrive search param
search_param = sys.argv[1]
# search for posts
posts_data = get_posts(search_param, auth[0])
print('Extracted {} posts.'.format(len(posts_data)))
# filter out c2c in results
print('Looking for C2C positions in them.')
c2c_posts = filter_c2c(posts_data)
# filter out already applied posts
new_posts = remove_applied_posts(c2c_posts, auth[1], auth[2])
# save the rest to positions.json
save_new_posts(new_posts)