#!/usr/bin/env python3
import multiprocessing as mp

import json

from common import utils
from common import client_system
from common.server import Server

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
  number_shared_lst = mp.Queue(maxsize=client_amount)
  log_file_name = "log"
  processes = []

  try:
    #load_from_file(client_array, server_result, winner_arr, file_name)
    utils.load_numbers_from_file(
      log_file_name,
      number_shared_lst,
    )

    print("Client database loaded successfully!")

  # else create new game
  except FileNotFoundError:

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
