import requests
from AutoClipper import Constants as Const
import schedule

'''
This is responsible for talking to the Twitch API to get appropriate internal representations of a channel:
    get_user_id(String channel_name):
        Given a channel name, returns user_id. 

    is_online(String channel_name):
        Given a channel name, return a bool indicating whether channel is online. 
'''

# curl -H 'Accept: application/vnd.twitchtv.v5+json' \
# -H 'Client-ID: uo6dggojyb8d6soh92zknwmi5ej1q2' \
# -X GET https://api.twitch.tv/kraken/users?login=dallas,dallasnchains

# Returns a user ID if the channel exists. To be used in finding out if channel is online.
def get_user_id(channel_name):

    URL = f'https://api.twitch.tv/kraken/users?login={channel_name}'

    response = requests.get(
        URL,
        headers={'Accept': 'application/vnd.twitchtv.v5+json', 'Client-ID': f'{Const.client_id}'}
    )

    '''FORMAT:
    {'_total': 1,
    'users': [{'display_name': 'Scarra',
     '_id': '22253819',
     'name': 'scarra',
     'type': 'user',
     'bio': '.',
     'created_at': '2011-05-07T09:53:48.159182Z',
     'updated_at': '2020-01-19T04:21:22.151436Z',
     'logo': 'https://static-cdn.jtvnw.net/jtv_user_pictures/8bd07ef046330084-profile_image-300x300.jpeg'}]}'''

    if len(response.json()['users']) > 0:
        user_id = response.json()['users'][0]['_id']
        return user_id
    else:
        NotADirectoryError("No channel with that name found")
    # We get the user ID and return it


# curl -H 'Accept: application/vnd.twitchtv.v5+json' \
# -H 'Client-ID: uo6dggojyb8d6soh92zknwmi5ej1q2' \
# -X GET 'https://api.twitch.tv/kraken/streams/44322889'

'''
Returns True if channel is live, False otherwise. Uses new Twitch API.
'''

def isOnline(channel_name):

    user_id = get_user_id(channel_name)

    URL = f'https://api.twitch.tv/helix/streams?user_id={user_id}'

    response = requests.get(
        URL,
        headers={'Client-ID': f'{Const.client_id}'},
    ).json()

    '''When offline:
    {'data': [], 'pagination': {}}'''

    # Returns True if 'stream' in JSON is None - this indicates that stream is offline.
    return not len(response['data']) == 0

if __name__ == '__main__':
    channel = 'arteezy'
    Const.user_id = get_user_id(channel)
    print(isOnline(channel))
    channel = 'xqcow'
    Const.user_id = get_user_id(channel)
    print(isOnline(channel))
    # Not a valid username:
    print(get_user_id('asdiasboudasnjdhabuisudqhwdqus') is None)
