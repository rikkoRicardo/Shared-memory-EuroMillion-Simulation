#!/usr/bin/env python3

from threading import Thread, Lock as threading_lock
import time
from .client import Client
from . import utils

#create backup components
client_database_backup = []
backup_file_path = ""


#function to create and store a new client
def create_client(client_shared_queue):
  global client_database_backup
  #5 numbers, 2 stars
  numbers = utils.get_ticket_structure()
  #create delay for simulation
  with threading_lock():
    #generate new client entry
    curr_client = Client(numbers)
    #append to backup list
    client_database_backup.append(curr_client.data_as_arr)
    client_shared_queue.put(curr_client.ticket_data)
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
    time.sleep(0.2)
    x.start()

  #pause main thread waiting for entries
  for thread in threads:
    thread.join()

  #save to be able to recover the game later
  utils.save_to_file(client_database_backup, save_file_path)


def define_winner(shared_queue):
  time.sleep(0.5)
  print("DRAWING WINNER", end="")
  time.sleep(0.5)

  winners = []
  while not shared_queue.empty():
    winners.append(shared_queue.get())

  #if there is any winners
  if len(winners):
    #list the ticket id because numbers match
    for ticket_number_data in winners:
      winner_id = find_client_by_ticket_num(ticket_number_data[0])

      utils.save_to_file(winner_id, backup_file_path)

      congrats_message = f"\n\nThe client with ticket ID {str(winner_id)} and numbers {ticket_number_data} won the EuroMillion "

      #check for jackpot
      if ticket_number_data[1]:
        print(congrats_message.join(" AND GOT THE JACKPOT!"))
      else:
        print(congrats_message)
  else:
    print("\n\nNo one won the EuroMillion this time, keep gambling!\n")


def find_client_by_ticket_num(ticket_number):
  global client_database_backup

  if not client_database_backup:
    print("Error: Server backup file is empty!\n")

  #search for a valid match
  if ticket_number in client_database_backup:
    index = client_database_backup.index(ticket_number)
    #return [self.ticket_id, self.ticket_data]
    return client_database_backup[index]

  print(f"Couldnt find anyone with ticket number {ticket_number}!\n")
  #else return not valid
  return -1
