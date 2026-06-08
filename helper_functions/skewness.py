from .avg import ft_avg
from .std import ft_std

def ft_skewness(array):
    avg = ft_avg(array)
    std = ft_std(array)
    if std == 0:
        return 0.0
    count = 0
    res = 0
    for x in array:
        res += ((x - avg) / std) ** 3
        count += 1
    return res / count
