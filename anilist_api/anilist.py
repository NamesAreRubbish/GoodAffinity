import requests
import json


def api_get_scores(username):
    query = '''
        query ($name: String) {
            MediaListCollection(userName: $name, type: ANIME) {
                lists {
                    isCustomList
                    entries {
                        mediaId
                        media {
                            idMal
                        }
                        score
                    }
                }
            }
        }
    '''

    variables = {'name': username}

    url = 'https://graphql.anilist.co'

    response = requests.post(url, json={'query': query, 'variables': variables})

    return json.loads(response.content.decode('utf-8'))['data']['MediaListCollection']


def repackage_data(json_data, mal_compatible):
    scores = {}

    for media_list in json_data['lists']:
        # Ignore custom list
        if media_list['isCustomList'] is False:
            # Add all non-zero scores
            for entry in media_list['entries']:
                if entry['score'] != 0:
                    if mal_compatible:
                        scores[entry['media']['idMal']] = entry['score']
                    else:
                        scores[entry['mediaId']] = entry['score']

    return scores

def get_users_scores_ani(username, mal_compatible=False):
    json_api_response = api_get_scores(username)
    scores = repackage_data(json_api_response, mal_compatible)
    return scores
