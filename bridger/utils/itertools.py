from typing import Dict, Iterable


def uniquify_dict_iterable(iterable: Iterable[Dict], unique_key: str) -> Iterable[Dict]:
    keys = list()
    for item in iterable:
        if key := item.get(unique_key):
            if key not in keys:
                keys.append(key)
                yield item
        else:
            yield item
