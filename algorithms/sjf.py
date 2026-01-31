def solve_sjf(processes):
    """
    Shortest Job First (SJF) 
    it is non-preemptive.
    at any moment, we pick the waiting process with the smallest burst time
    """
    processes.sort(key=lambda x: x.arrival_time)
    current_time = 0
    completed = []
    gantt_log = []
    
    #we loop until every process is in the 'completed' list
    while len(completed) < len(processes):
        
        #step 1: find all processes that have arrived by now
        available_processes = []
        for p in processes:
            if p.arrival_time <= current_time and p not in completed:
                available_processes.append(p)
        
        #step 2: handle idle CPU
        if not available_processes:
            #no process available? jump to the next arrival time.
            remaining = [p for p in processes if p not in completed]
            if remaining:
                next_arrival = min(remaining, key=lambda x: x.arrival_time).arrival_time
                current_time = next_arrival
                continue
        
        #step 3: pick the shortest job
        #if burst times are equal, I use arrival time as a tie-breaker.
        shortest_job = min(available_processes, key=lambda x: (x.burst_time, x.arrival_time, x.pid))
        p = shortest_job
        
        #step 4: execute the chosen process fully
        p.start_time = current_time
        p.response_time = p.start_time - p.arrival_time
        
        completion_time = current_time + p.burst_time
        p.completion_time = completion_time
        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time
        
        gantt_log.append((current_time, completion_time, p.pid))
        completed.append(p)
        current_time = completion_time
        
    return gantt_log