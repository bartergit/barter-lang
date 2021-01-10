def rfind(lst, sought_elt):
    for r_idx, elt in enumerate(reversed(lst)):
        if elt == sought_elt:
            return len(lst) - 1 - r_idx
    return -1


def find(lst, el):
    try:
        return lst.index(el)
    except ValueError:
        return -1


