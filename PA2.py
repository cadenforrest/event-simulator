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
        self.completion_time = arrival_time + service_time

class Event(): 
    def __init__(self, type, time):
        self.type = type # 0: arrival, 1: departure
        self.time = time
        self.completion_time = 0
        self.arrival_time = 0
        self.service_time = 0 

class State(): 
    def __init__(self, serverIdle, readyQueueCount):
        self.serverIdle = serverIdle
        self.readyQueueCount = readyQueueCount
        self.clock = 0

def calculate_average_turnaround_time(allEvents): 
    total_turnaround_time = 0
    for event in allEvents: 
        if event.completion_time > 0: 
            total_turnaround_time += event.completion_time - event.time
    return total_turnaround_time/len(allEvents)

def calculate_total_throughput(total_time, completed_processes): 
    return completed_processes / total_time 

def calculate_average_utilization(serverStates): 
    numTrue = 0
    for state in serverStates: 
        if state == True: 
            numTrue += 1
    return numTrue/len(serverStates)

def calculate_average_number_of_processes_in_event_queue(allQueueSizes): 
    i = 0
    for queueSize in allQueueSizes: 
        i += queueSize
    return i/len(allQueueSizes)

def initialize(lambda_): 
    state = State(True, 0)
    eventQueue = []
    # get t by the current clock + an interarrival time X, and we can assume X is a random variable
    # following an Exponential Distribution, given the average arrival rate lambda or the average 
    # interarrival time 1 / lambda
    t = state.clock + generate_interarrival_time(lambda_)
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
        service_time = generate_service_time()
        schedule_event(1, event.time+service_time, eventQueue)
        event.completion_time = event.time + service_time

def run(lambda_): 
    eventQueue, state = initialize(lambda_)
    completed_processes = 0
    serverStates = []
    allEvents = []
    allQueueSizes = []
    completedEvents = []
    while eventQueue and completed_processes < 10000:
        event = eventQueue.pop(0)
        state.clock = event.time
        if event.type == 0:
            arrival_handler(event, state, eventQueue, lambda_)
        else:
            dep_handler(event, state, eventQueue)
            completed_processes += 1
            completedEvents.append(event)
        allEvents.append(event)
        serverStates.append(state.serverIdle) 
        allQueueSizes.append(state.readyQueueCount)

    print("Average Arrival Rate: ", str(lambda_))
    print("Average CPU Utilization: ", calculate_average_utilization(serverStates))
    print("Total throughput: ", calculate_total_throughput(state.clock, completed_processes), "per unit time")
    print("Total units time: ", state.clock)
    print("Average Turnaround Time of processes: ", calculate_average_turnaround_time(completedEvents))
    print("Average number of processes in Ready Queue: ", calculate_average_number_of_processes_in_event_queue(allQueueSizes))
    return calculate_average_utilization(serverStates), calculate_total_throughput(state.clock, completed_processes), calculate_average_turnaround_time(completedEvents), calculate_average_number_of_processes_in_event_queue(allQueueSizes)

def plot_data(): 
    utilizations = []
    throughputs = []
    turnaround_times = []
    averages_in_ready_queue = []

    for lambda_ in range(10, 30): 
        utilization, throughput, turnaround_time, average_in_ready_queue = run(lambda_) 
        utilizations.append([utilization, lambda_])
        throughputs.append([throughput, lambda_])
        turnaround_times.append([turnaround_time, lambda_])
        averages_in_ready_queue.append([average_in_ready_queue, lambda_])
    
    # PLOTS
    util_fig = plt.figure()
    ax = util_fig.add_subplot(1, 1, 1)
    ax.plot([x[1] for x in utilizations], [x[0] for x in utilizations])
    ax.set_title("Utilization vs. Lambda")
    ax.set_xlabel("Lambda")
    ax.set_ylabel("Utilization")
    util_fig.savefig("utilization.png")
    plt.show()
    
    throughput_fig = plt.figure()
    ax = throughput_fig.add_subplot(1, 1, 1)
    ax.plot([x[1] for x in throughputs], [x[0] for x in throughputs])
    ax.set_title("Throughput vs. Lambda")
    ax.set_xlabel("Lambda")
    ax.set_ylabel("Throughput")
    throughput_fig.savefig("throughput.png")
    plt.show()

    turnaround_fig = plt.figure()
    ax = turnaround_fig.add_subplot(1, 1, 1)
    ax.plot([x[1] for x in turnaround_times], [x[0] for x in turnaround_times])
    ax.set_title("Turnaround Time vs. Lambda")
    ax.set_xlabel("Lambda")
    ax.set_ylabel("Turnaround Time")
    turnaround_fig.savefig("turnaround_time.png")
    plt.show()

    average_in_ready_queue_fig = plt.figure()
    ax = average_in_ready_queue_fig.add_subplot(1, 1, 1)
    ax.plot([x[1] for x in averages_in_ready_queue], [x[0] for x in averages_in_ready_queue])
    ax.set_title("Average in Ready Queue vs. Lambda")
    ax.set_xlabel("Lambda")
    ax.set_ylabel("Average in Ready Queue")
    average_in_ready_queue_fig.savefig("average_in_ready_queue.png")
    plt.show()

  
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--plot', action='store_true')
    parser.add_argument("--average-arrival-rate", type=int, default = 10)
    parser.add_argument("--average-service-time", type=float)
    args = parser.parse_args()
    if args.plot: 
        plot_data()
        exit()

    lambda_ = args.average_arrival_rate
    run(lambda_)
    print("Done")