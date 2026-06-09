import math

def ft_percentile(array, value):
    if not isinstance(array, (tuple, list)):
        raise TypeError("Input must be a tulpe or list")
    if not array:
        raise ValueError("Input cannot be empty")
    for x in array:
        if not isinstance(x, (int, float)):
            raise TypeError("All elements must be numbers")
    if not isinstance(value, int):
        raise ValueError("input needs to be between 1 and 100")
    sorted_array = sorted(array)
    len_array = len(array)
    raw_pos = (len_array * value / 100)
    if raw_pos != int(raw_pos):
        return sorted_array[int(raw_pos)]
    else:
        return (sorted_array[int(raw_pos)] + sorted_array[int(raw_pos- 1)]) / 2

# test = [1,2,3,4,5]
# # print(test[6])
# # print(len(test))
# print(f"25: {ft_percentile(test, 25)}")
# print(f"50: {ft_percentile(test, 50)}")
# print(f"75: {ft_percentile(test, 75)}")
