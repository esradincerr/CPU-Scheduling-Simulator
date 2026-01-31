def solve_priority_np(processes):
    """
    Priority Scheduling 
    non-preemptive
    we select the process with the highest priority (lowest numerical value)
    once it starts, it runs until completion
    """
    processes.sort(key=lambda x: x.arrival_time)
    current_time = 0
    completed = []
    gantt_log = []
    
    while len(completed) < len(processes):
        #step 1: filter available processes
        available_processes = []
        for p in processes:
            if p.arrival_time <= current_time and p not in completed:
                available_processes.append(p)
        
        if not available_processes:
            remaining = [p for p in processes if p not in completed]
            if remaining:
                next_arrival = min(remaining, key=lambda x: x.arrival_time).arrival_time
                current_time = next_arrival
                continue
        
        #step 2: select based on priority
        #lower value = higher priority. tie-breaker is arrival time.
        highest_prio_job = min(available_processes, key=lambda x: (x.priority, x.arrival_time, x.pid))
        p = highest_prio_job
        
        #step 3: execute fully
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