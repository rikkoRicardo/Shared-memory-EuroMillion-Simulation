#!/usr/bin/env python3
import threading
from dataclasses import dataclass
from . import utils
import time

import numpy as np


@dataclass
class Server:
  _client_numbers: int
  _results: int

  def __init__(self):
    self.clients = []
    self.results = []
    self.draw_condition = threading.Condition()
    self.lock = threading.Lock()
    self.results_event = threading.Event()

  def accept_player(self, list):
    with self.lock:
      self.clients.append(list)

  def check_results(self, shared_queue):
    JACKPOT = True
    with self.lock:
      for player_numbers in self.clients:
        incoming_guess = np.array(player_numbers[0])
        incoming_star_guess = np.array(player_numbers[1])
        print(incoming_guess == self.results.numbers)
        #match player number
        if incoming_guess == self.results.numbers:
          #check for jackpot by checking stars
          if incoming_star_guess == self.results.stars:
            shared_queue.put([player_numbers, JACKPOT])
            return

        shared_queue.put([player_numbers, not JACKPOT])

  def draw_numbers(self):
    with self.draw_condition:
      if not self.results:
        self.results = np.array(utils.get_ticket_structure())
        self.results.stars = self.results[1]
        self.results.numbers = self.results[0]
        time.sleep(0.5)
        print(f"\nTICKET WINNER: {self.results}\n")
        self.results_event.set()  # Notify waiting clients

  def run(self, shared_queue):
    threads = []

    while not shared_queue.empty():
      thread = threading.Thread(target=self.accept_player,
                                args=(shared_queue.get(), ))
      threads.append(thread)
      thread.start()

    for thread in threads:
      thread.join()

    self.draw_numbers()
    self.results_event.wait()

    self.check_results(shared_queue)