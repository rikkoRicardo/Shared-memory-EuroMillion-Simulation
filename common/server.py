#!/usr/bin/env python3
import threading
from dataclasses import dataclass


@dataclass
class Server:
  __client_numbers: int
  __results: int

  def __init__(self, client_list):
    self.__clients = []
    self.__results = []
    self.__lock = threading.lock()

  def accept_player(self, list):
    with self.lock:
      self.__clients.append()


#massive to do
"""
The idea is when the program starts, the server will wait for client bets for a number of x seconds, then it will grab the client guesses from the shared memory area, then another process is started to create a winning sample and check for winners
"""
