def flatten_results(results: list, key: str) -> list:
    for idx, item in enumerate(results):
        value = item[1]
        results[idx] = results[idx][0]
        setattr(results[idx], key, value)
    return results
