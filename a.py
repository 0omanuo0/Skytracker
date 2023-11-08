# import threading
# import random
# import math
# from concurrent.futures import ProcessPoolExecutor

# def loop():
#     a = [random.random() for i in range(1000)]
#     while True:
#         a = [a, a, sum([math.sqrt(i) for i in range(1, random.randint(1000,10000))])]

# if __name__ == '__main__':
#     # report a message
#     print('Starting task...')
#     # create the process pool
#     with ProcessPoolExecutor(61) as exe:
#         # perform calculations
#         results = exe.map(loop, range(1,50000))
#     # report a message
#     print('Done.')

from multiprocessing import Pool, cpu_count
import math
import random

def random_calculation(x):
    while True:
        a = x*x

p = Pool(processes=cpu_count())
p.map(random_calculation, range(cpu_count()))
a = [random.random() for i in range(1000)]

while True:
    a = [a, a, sum([math.sqrt(i) for i in range(1, random.randint(1000,10000))])]

