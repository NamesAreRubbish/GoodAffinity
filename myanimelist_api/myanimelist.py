import requests
import json
import time


def api_get_scores(username, page):
    url = 'https://api.jikan.moe/v3/user/{0}/animelist/all/{1}'.format(username, page)

    response = requests.get(url)

    json_data = json.loads(response.content.decode('utf-8'))

    if json_data['anime']:
        return json_data
    else:
        return None


def repackage_data(json_data, scores):
    for anime in json_data['anime']:
        # Add all non-zero scores
        if anime['score'] != 0:
            scores[anime['mal_id']] = anime['score']

    return scores

def get_users_scores_mal(username):
    current_page = 1
    scores = {}
    while True:
        # Wait to prevent rate limiting
        time.sleep(.5)
        api_response_data = api_get_scores(username, current_page)
        if api_response_data:
            scores = repackage_data(api_response_data, scores)
            current_page += 1
        else:
            break

    return scores
