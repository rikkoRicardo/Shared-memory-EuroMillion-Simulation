#!/usr/bin/env python3
import multiprocessing as mp

from common.utils import load_old_game_state
from common import client_system
from common.server import Server

import sys

logo = """

,------.                      ,--.   ,--.,--.,--.,--.,--.              
|  .---',--.,--.,--.--. ,---. |   `.'   |`--'|  ||  |`--' ,---. ,--,--,  
|  `--, |  ||  ||  .--'| .-. ||  |'.'|  |,--.|  ||  |,--.| .-. ||      \ 
|  `---.'  ''  '|  |   ' '-' '|  |   |  ||  ||  ||  ||  |' '-' '|  ||  | 
`------' `----' `--'    `---' `--'   `--'`--'`--'`--'`--' `---' `--''--' 
                                                          Ricardo - 2023 
"""

if __name__ == "__main__":
  print(logo)

  #setup basic properties
  client_amount = 20
  log_file_name = "log"

  try:
    clients = []
    server_result = []
    winners = [] 
    
    load_old_game_state(clients, server_result, winners, log_file_name)
    
    print("Log file found, Loading last game state")
    time.sleep(2
              )
    print(f"The EuroMillion result was {server_result}")
    
    if winners:
      for winner in winners:
        print(f"{(ticket_id:=winner[0])} won with the ticket {(ticket_number:=winner[1])} ")
    else:
        print("There was no winners")

    print("Please come back on the next round of EuroMillion!!")
    
  # else create new game
  except FileNotFoundError:
    
    number_shared_lst = mp.Queue(maxsize=client_amount)
    processes = []
    
    #start by declaring client process
    list_system_process = mp.Process(target=client_system.create_list,
                                     args=(number_shared_lst, client_amount,
                                           log_file_name))

    processes.append(list_system_process)

    #declare and start server process
    server = Server()

    server_process = mp.Process(target=server.run, args=(number_shared_lst, ))
    processes.append(server_process)

    #start client process and wait
    list_system_process.start()
    list_system_process.join()

    #start server process and wait
    server_process.start()
    server_process.join()

    client_system.define_winner(number_shared_lst)

    #terminate process and free process handle
    for process in processes:
      process.terminate()
      process.close()
