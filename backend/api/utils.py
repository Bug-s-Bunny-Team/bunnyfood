from typing import Optional

import requests
# from instaloader import Instaloader, ProfileNotExistsException, InstaloaderException
# from instaloader import Profile as InstaProfile

__all__ = ['flatten_results', 'search_social_profile']

# _client = Instaloader()


def flatten_results(results: list, key: str) -> list:
    for idx, item in enumerate(results):
        value = item[1]
        results[idx] = results[idx][0]
        setattr(results[idx], key, value)
    return results


# TODO: does it make sense to move this into its own lambda?
# def search_social_profile(username: str) -> Optional[InstaProfile]:
#     try:
#         profile = InstaProfile.from_username(_client.context, username)
#         return profile
#     except (InstaloaderException, ProfileNotExistsException):
#         return None


def search_social_profile(username: str) -> bool:
    r = requests.post(
        'https://gramhir.com/app/controllers/ajax.php',
        data={'query': username, 'type': 'search_api'},
    )
    return r.status_code == 200
