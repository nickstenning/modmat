from collections import defaultdict

def histogram(list_of_lists, f=len):
    hist = defaultdict(lambda: 0)
    for item in list_of_lists:
        hist[f(item)] += 1
    return [hist[i] for i in xrange(max(hist.keys()) + 1)]

def truncate_or_pad(ary, n, pad=None):
    if len(ary) < n:
        return ary + [pad] * (n - len(ary))
    else:
        return ary[:n]
