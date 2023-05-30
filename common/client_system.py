#!/usr/bin/env python3

from threading import Thread, Lock as threading_lock
import time, random
from .client import Client
from . import utils

#create backup components
client_database_backup = []
backup_file_path = ""


#function to create and store a new client
def create_client(client_shared_queue):
  global client_database_backup
  #5 numbers, 2 stars
  numbers = [random.sample(range(1, 51), 5), random.sample(range(1, 12), 2)]

  with threading_lock():
    #generate new client entry
    curr_client = Client(numbers)
    #append to backup list
    client_database_backup.append(curr_client.data_as_arr)
    client_shared_queue.put(curr_client.ticket_data)
    #create delay for simulation
    time.sleep(0.1)
    #notify new client entry
    print(f"NEW ENTRY - ID: {str(curr_client.ticket_id)} saved successfully!")


#structure list to be sent to the server
def create_list(shared_client_queue, client_amount, save_file_path):
  #declare backup components
  global backup_file_path
  backup_file_path = save_file_path

  #create thread list
  threads = []

  #create one thread for each client
  for index in range(client_amount):
    x = Thread(target=create_client,
               args=(shared_client_queue, ),
               name="cl_entry_thread")
    threads.append(x)
    x.start()

  #pause main thread waiting for entries
  for thread in threads:
    thread.join()

  #save to be able to recover the game later
  utils.save_to_file(str(client_database_backup), save_file_path)


def find_client_by_ticket_num(ticket_number, file):
  #get backup components
  global client_database_backup, backup_file_path

  #check for a valid list
  if not client_database_backup:
    utils.load_full_from_file(backup_file_path)

  #search for a valid match
  if ticket_number in client_database_backup:
    index = client_database_backup.index(ticket_number)
    #return ticket id
    return client_database_backup[index][0]

  #else return not valid
  return -1
