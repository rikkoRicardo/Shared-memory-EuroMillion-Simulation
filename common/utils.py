#!/usr/bin/env python3
import random


def load_numbers_from_file(file_path, queue):

  #open file and get text
  with open(file_path, "r") as f:
    recieved_text = eval(f.read())

    for each_entry in recieved_text:
      queue.put(each_entry[0], block=False)


def load_full_from_file(file_path, queue):

  #open file and get text
  with open(file_path, "r") as f:
    recieved_text = eval(f.read())

    for each_entry in recieved_text:
      queue.put(each_entry, block=False)


def save_to_file(data, file_name):
  file = open(file_name, "w")
  file.write(data)
  file.close()


def get_ticket_structure():
  return [random.sample(range(1, 51), 5), random.sample(range(1, 12), 2)]
