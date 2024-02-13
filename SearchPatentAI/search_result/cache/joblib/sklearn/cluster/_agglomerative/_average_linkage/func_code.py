# first line: 709
def _average_linkage(*args, **kwargs):
    kwargs["linkage"] = "average"
    return linkage_tree(*args, **kwargs)
