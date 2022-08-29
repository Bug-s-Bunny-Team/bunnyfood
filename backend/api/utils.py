import requests

__all__ = ['flatten_results', 'search_social_profile']


def flatten_results(results: list, key: str) -> list:
    for idx, item in enumerate(results):
        value = item[1]
        results[idx] = results[idx][0]
        setattr(results[idx], key, value)
    return results


def search_social_profile(username: str) -> bool:
    r = requests.post(
        'https://gramhir.com/app/controllers/ajax.php',
        data={'query': username, 'type': 'search_api'},
    )
    return r.status_code == 200
