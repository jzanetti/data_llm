def replace_substrings(string, substrings):
    for substr in substrings:
        string = string.replace(substr, "")
    return string
