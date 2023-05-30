#!/usr/bin/env python3
import threading
from dataclasses import dataclass
from . import utils
import time


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
        print(player_numbers)

        #match player number
        if player_numbers[0] is self.results[0]:
          #check for jackpot by checking stars
          if player_numbers[1] is self.results[1]:

            return

          shared_queue.put([player_numbers, not JACKPOT])

      shared_queue.put([player_numbers, JACKPOT])

   

  def draw_numbers(self):
    with self.draw_condition:
      if not self.results:
        self.results = utils.get_ticket_structure()
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


#massive to do
"""
The idea is when the program starts, the server will wait for client bets for a number of x seconds, then it will grab the client guesses from the shared memory area, then another process is started to create a winning sample and check for winners
"""
