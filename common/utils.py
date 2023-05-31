#!/usr/bin/env python3
import random
import pickle
import os.path


# Data Saved during execution -> client array, server result arr, winner array
def save_to_file(data, file_name):
  with open(file_name, "ab+") as f:
    pickle.dump(data, f)


# Data Loaded in order -> client array, server result arr, winner array
def load_old_game_state(client_array, server_result, winner_arr, file_name):
 
  if os.path.exists(file_name):
    with open(file_name, "rb") as f:
      client_array.append(pickle.load(f))
      server_result.append(pickle.load(f))
      winner_arr.append(pickle.load(f))
  else:
    raise FileNotFoundError


def get_ticket_structure():
  
  return [random.sample(range(1, 51), 5), [random.sample(range(1, 12), 2)]]
