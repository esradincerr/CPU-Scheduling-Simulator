def solve_fcfs(processes):
    """
    First-Come First-Served
    this is the simplest algorithm. processes run in the order they arrive.
    it is non-preemptive, meaning once a process starts, it finishes.
    """
    #step 1: sort by arrival time 
    processes.sort(key=lambda x: x.arrival_time)
    
    current_time = 0
    gantt_log = []
    
    for p in processes:
        #if the CPU is idle (no process has arrived yet), jump to the arrival time
        if current_time < p.arrival_time:
            current_time = p.arrival_time
            
        #record the start time and calculate response time
        p.start_time = current_time
        p.response_time = p.start_time - p.arrival_time
        
        #since it's non-preemptive, we just add the burst time to current time
        completion_time = current_time + p.burst_time
        p.completion_time = completion_time
        
        #calculate stats: Turnaround = Completion - Arrival
        p.turnaround_time = p.completion_time - p.arrival_time
        #Waiting = Turnaround - Burst
        p.waiting_time = p.turnaround_time - p.burst_time
        
        #save this execution interval (start, end, pid) to the log so we can draw the chart later
        gantt_log.append((current_time, completion_time, p.pid))
        
        #update the current system time to be the completion time of this process, ready for the next one
        current_time = completion_time

    return gantt_log