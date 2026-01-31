def solve_priority_p(processes):
    """
    Priority Scheduling 
    Preemptive
    if a new process arrives with a higher priority (lower value) than the current one,
    the CPU stops the current process and switches to the new one
    """
    for p in processes:
        p.remaining_time = p.burst_time

    current_time = 0
    completed = 0
    n = len(processes)
    gantt_log = []
    
    while completed < n:
        #step 1: check available processes
        available = [p for p in processes if p.arrival_time <= current_time and p.remaining_time > 0]
        
        if not available:
            current_time += 1
            continue
            
        #step 2: select process with highest priority
        highest_prio = min(available, key=lambda x: (x.priority, x.arrival_time))
        
        if highest_prio.start_time == -1: 
             highest_prio.start_time = current_time
             highest_prio.response_time = highest_prio.start_time - highest_prio.arrival_time

        #step 3: log execution (combine logs if same process continues)
        if gantt_log and gantt_log[-1][2] == highest_prio.pid:
            last_entry = gantt_log[-1]
            gantt_log[-1] = (last_entry[0], current_time + 1, last_entry[2])
        else:
            gantt_log.append((current_time, current_time + 1, highest_prio.pid))

        #run for 1 unit
        highest_prio.remaining_time -= 1
        current_time += 1
        
        if highest_prio.remaining_time == 0:
            completed += 1
            highest_prio.completion_time = current_time
            highest_prio.turnaround_time = highest_prio.completion_time - highest_prio.arrival_time
            highest_prio.waiting_time = highest_prio.turnaround_time - highest_prio.burst_time

    return gantt_log