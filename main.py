#!/usr/bin/env python3
import multiprocessing as mp

from common import utils
from common import client_system
#from common.server import Server

logo = """

,------.                      ,--.   ,--.,--.,--.,--.,--.              
|  .---',--.,--.,--.--. ,---. |   `.'   |`--'|  ||  |`--' ,---. ,--,--,  
|  `--, |  ||  ||  .--'| .-. ||  |'.'|  |,--.|  ||  |,--.| .-. ||      \ 
|  `---.'  ''  '|  |   ' '-' '|  |   |  ||  ||  ||  ||  |' '-' '|  ||  | 
`------' `----' `--'    `---' `--'   `--'`--'`--'`--'`--' `---' `--''--' 
                                                          Ricardo - 2023 
"""

client_amount = 2
number_shared_lst = mp.Queue(maxsize=client_amount)
log_file_name = "log"
processes = []

if __name__ == "__main__":
  print(logo)

  #Load past game if existent
  try:
    utils.load_numbers_from_file(
      log_file_name,
      number_shared_lst,
    )

    print("Client database loaded successfully!")

  # else create a new one
  except FileNotFoundError:
    list_system_process = mp.Process(target=client_system.create_list,
                                     args=(number_shared_lst, client_amount,
                                           log_file_name))
    processes.append(list_system_process)
    list_system_process.start()
    list_system_process.join()

  finally:
    #start server process
    print("\nServer started!")

  #terminate process and free process handle
  for process in processes:
    process.terminate()
    process.close()
