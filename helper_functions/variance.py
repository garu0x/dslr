from .avg import ft_avg

def ft_variance(array):
    avg = ft_avg(array)
    res = 0
    count = 0
    for x in array:
        res += (x - avg) ** 2
        count += 1
    return res / count
