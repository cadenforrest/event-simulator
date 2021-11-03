import argparse
import json
import matplotlib.pyplot as plt
import random

AVERAGE_SERVICE_TIME = 0.04

#TODO: add a function to plot the results
#TODO: generate interarrival times 

class Process(): 
    def __init__(self, arrival_time, service_time):
        self.arrival_time = arrival_time
        self.service_time = service_time

class Event(): 
    def __init__(self, type, time, process=None):
        self.type = type # 0: arrival, 1: departure
        self.time = time
        self.process = process

class State(): 
    def __init__(self, serverIdle, readyQueueCount):
        self.serverIdle = serverIdle
        self.readyQueueCount = readyQueueCount
        self.clock = 0

def initialize(lambda_): 
    state = State(True, 0)
    eventQueue = []
    # get t by the current clock + an interarrival time X, and we can assume X is a random variable
    # following an Exponential Distribution, given the average arrival rate lambda or the average 
    # interarrival time 1 / lambda
    t = state.clock + random.expovariate(1 / lambda_)
    schedule_event(0, t, eventQueue)
    return eventQueue, state

def schedule_event(type, time, eventQueue): 
    event = Event(type, time)
    eventQueue.append(event)
    eventQueue.sort(key=lambda event: event.time) # insert e into eventQueue at eq_head and sort w.r.t. time

def generate_interarrival_time(lambda_): 
    return random.expovariate(1 / lambda_)

def generate_service_time():
    return random.expovariate(AVERAGE_SERVICE_TIME)

def arrival_handler(event, state, eventQueue, lambda_):
    if state.serverIdle: 
        state.serverIdle = False
        schedule_event(1, event.time+generate_service_time(), eventQueue)
    else: 
        state.readyQueueCount += 1

    schedule_event(0, event.time+generate_interarrival_time(lambda_), eventQueue)

def dep_handler(event, state, eventQueue):
    if state.readyQueueCount == 0: 
        state.serverIdle = True
    else:
        state.readyQueueCount -= 1
        schedule_event(1, event.time+generate_service_time(), eventQueue)
        
def run(lambda_): 
    eventQueue, state = initialize(lambda_)
    completed_processes = 0
    while eventQueue and completed_processes < 10000:
        event = eventQueue.pop(0)
        state.clock = event.time
        if event.type == 0:
            arrival_handler(event, state, eventQueue, lambda_)
        else:
            dep_handler(event, state, eventQueue)
            completed_processes += 1
        print(state.clock, state.serverIdle, state.readyQueueCount)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--average-arrival-rate", type=int, default = 10)

    args = parser.parse_args()
    lambda_ = args.average_arrival_rate
    run(lambda_)
    print("Done")