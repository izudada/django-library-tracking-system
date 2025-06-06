import random
rand_list = [random.randrange(1,20, 1) for i in range(1,20) ]


list_comprehension_below_10 =[i for i in range(0,10) if i < 10]

list_comprehension_below_10 = list(filter(lambda x: x < 10, range(0,10)))