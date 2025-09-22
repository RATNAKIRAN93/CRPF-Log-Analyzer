#!/usr/bin/env python3
import time, random
levels = ["INFO","WARN","ERROR","DEBUG"]
while True:
    print(f"{time.strftime('%b %d %H:%M:%S')} myhost myapp[{random.randint(1000,9999)}]: {random.choice(levels)} - demo log {random.random()}")
    time.sleep(0.5)
