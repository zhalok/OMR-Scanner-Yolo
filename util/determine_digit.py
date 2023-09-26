def determine_digit(y):
    pos_list = [140 + 70 * i for i in range(10)]
    ans = 10000
    idx = None
    for index, i in enumerate(pos_list):
        if abs(y - i) < ans:
            ans = abs(y - i)
            idx = index
    return idx
