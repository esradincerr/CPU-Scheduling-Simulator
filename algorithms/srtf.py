def solve_srtf(processes):
    """
    Shortest Remaining Time First (SRTF)
    this is the preemptive version of SJF
    we check every second if a new process with a shorter remaining time has arrived
    """
    #initialize remaining time for all processes
    for p in processes:
        p.remaining_time = p.burst_time

    current_time = 0
    completed = 0
    n = len(processes)
    gantt_log = []
    
    #we simulate time second by second
    while completed < n:
        #step 1: find available processes that are not finished
        available = [p for p in processes if p.arrival_time <= current_time and p.remaining_time > 0]
        
        #if no process is available, just advance time
        if not available:
            current_time += 1
            continue
            
        #step 2: pick the process with the minimum remaining time
        shortest = min(available, key=lambda x: (x.remaining_time, x.arrival_time))
        
        #if it's the first time this process runs, record start time
        if shortest.start_time == -1: 
             shortest.start_time = current_time
             shortest.response_time = shortest.start_time - shortest.arrival_time

        #step 3: log the execution
        #if we continue running the same process, we update the last log entry
        #instead of creating a new one (makes the chart look cleaner).
        if gantt_log and gantt_log[-1][2] == shortest.pid:
            last_entry = gantt_log[-1]
            gantt_log[-1] = (last_entry[0], current_time + 1, last_entry[2])
        else:
            gantt_log.append((current_time, current_time + 1, shortest.pid))

        #step 4: run for exactly 1 unit of time
        shortest.remaining_time -= 1
        current_time += 1
        
        #step 5: check if the process finished
        if shortest.remaining_time == 0:
            completed += 1
            shortest.completion_time = current_time
            shortest.turnaround_time = shortest.completion_time - shortest.arrival_time
            shortest.waiting_time = shortest.turnaround_time - shortest.burst_time

    return gantt_log