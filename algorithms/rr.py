def solve_rr(processes, quantum):
    """
    Round Robin (RR) Scheduling
    this uses a queue and a time quantum
    each process runs for a small slice of time, then goes to the back of the line
    """
    #reset remaining times just in case
    for p in processes:
        p.remaining_time = p.burst_time

    processes.sort(key=lambda x: x.arrival_time)
    current_time = 0
    gantt_log = []
    queue = []
    remaining_processes = processes[:] #I make a copy to manage arrivals safely
    
    #step 1: add processes that have arrived at t=0 to the queue
    while remaining_processes and remaining_processes[0].arrival_time <= current_time:
        queue.append(remaining_processes.pop(0))
        
    while queue or remaining_processes:
        #handle the case where queue is empty but more processes are coming later
        if not queue:
            if remaining_processes:
                current_time = remaining_processes[0].arrival_time
                while remaining_processes and remaining_processes[0].arrival_time <= current_time:
                    queue.append(remaining_processes.pop(0))
            continue

        #step 2: take the first process from the queue
        p = queue.pop(0)
        
        if p.start_time == -1:
            p.start_time = current_time
            p.response_time = p.start_time - p.arrival_time

        #step 3: run for quantum or remaining time 
        exec_time = min(quantum, p.remaining_time)
        gantt_log.append((current_time, current_time + exec_time, p.pid))
        
        p.remaining_time -= exec_time
        current_time += exec_time
        
        #step 4: check for new arrivals during this execution
        #new arrivals must enter the queue before the current process re-enters
        while remaining_processes and remaining_processes[0].arrival_time <= current_time:
            queue.append(remaining_processes.pop(0))
            
        #step 5: if process is not done, put it back in queue
        if p.remaining_time > 0:
            queue.append(p)
        else:
            #process is done
            p.completion_time = current_time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time

    return gantt_log