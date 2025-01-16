import flickrapi

API_KEY = '90e5b18fec35cb89dd97917352ee320c'
API_SECRET = '079ff665c326875a'

# Initialize the Flickr API client
flickr = flickrapi.FlickrAPI(API_KEY, API_SECRET, format='parsed-json')

# Replace with the Flickr username
username = 'Cushing Memorial Library and Archives, Texas A&M'

# Get user ID from username
user_info = flickr.people.findByUsername(username=username)
user_id = user_info['user']['nsid']
print(user_id)

# Fetch photos uploaded by the user
photos = []
page = 1
pages = 3
while page <= pages:
    response = flickr.photos.search(user_id=user_id, page=page, per_page=500)
    # print(response)
    photos += response['photos']['photo']
    if page >= response['photos']['pages']:
        break
    page += 1


for photo in photos:
    response=flickr.photos.getInfo(photo_id=photo['id'])
    print(response)
# Display photo details
# for photo in photos:
#     # print(f"Title: {photo['title']}, ID: {photo['id']}")
#     for thing in photo.items():
#         print(thing)
# # Custom URL to resolve
# custom_url = 'https://flickr.com/photos/cushinglibrary'
#
# # Resolve the user information
# user_info = flickr.urls.lookupUser(url=custom_url)
#
# # Extract user ID and username
# user_id = user_info['user']['id']
# username = user_info['user']['username']['_content']
#
# print(f"User ID: {user_id}, Username: {username}")