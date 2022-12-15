#!/usr/bin/python3

from pynput import keyboard
import time
import logging


class Timer:
    previous_time = None

    def __init__(self) -> None:
        self.previous_time = time.perf_counter()

    def step(self) -> float:
        delta: float = time.perf_counter() - self.previous_time
        self.previous_time = time.perf_counter()
        return delta


timer = Timer()


def on_press(key):
    try:
        print(key.char, end='\t')
        print(timer.step())
    except AttributeError:
        print(key, end='\t')
        print(timer.step())


if __name__ == "__main__":
    try:
        with keyboard.Listener(
                on_press=on_press) as listener:
            listener.join()
    except KeyboardInterrupt:
        print("\nBye o/")
