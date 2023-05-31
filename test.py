import multiprocessing as mp
import time

shared_q = mp.Queue(maxsize=10)


def put_on_list(shared_queue, number):
  shared_queue.put(10)
  shared_queue.put(20)


def take_off_list(shared_queue):
  while not shared_queue.empty():
    var = shared_queue.get()
    print(var)


process1 = mp.Process(target=put_on_list, args=(
  shared_q,
  30,
))
process2 = mp.Process(target=take_off_list, args=(shared_q, ))
process1.start()
process2.start()
process1.join()
process2.join()
