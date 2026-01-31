import itertools

def print_stats(processes, gantt_log=None):
    """
    this function prints the final table with Turnaround, Waiting, and Response times
    it also counts the total context switches if the log is provided
    """
    #I defined fixed widths for columns 
    w_pid = 5
    w_arr = 9
    w_burst = 7
    w_compl = 12
    w_turn = 12
    w_wait = 9
    w_resp = 9

    #step 1: print the table header 
    print(f"{'PID':<{w_pid}} {'Arrival':<{w_arr}} {'Burst':<{w_burst}} {'Completion':<{w_compl}} {'Turnaround':<{w_turn}} {'Waiting':<{w_wait}} {'Response':<{w_resp}}")
    print("-" * 75)
    
    total_wait = 0
    total_turnaround = 0
    total_response = 0
    
    #step 2: print stats for each process
    for p in processes:
        print(f"{p.pid:<{w_pid}} {p.arrival_time:<{w_arr}} {p.burst_time:<{w_burst}} {p.completion_time:<{w_compl}} {p.turnaround_time:<{w_turn}} {p.waiting_time:<{w_wait}} {p.response_time:<{w_resp}}")
        
        #sum up the values to calculate averages later
        total_wait += p.waiting_time
        total_turnaround += p.turnaround_time
        total_response += p.response_time
        
    n = len(processes)
    print("-" * 75)
    
    #step 3: print averages
    if n > 0:
        #I use .2f to show 2 decimal places for better precision
        print(f"Average Turnaround Time: {total_turnaround / n:.2f}")
        print(f"Average Waiting Time:    {total_wait / n:.2f}")
        print(f"Average Response Time:   {total_response / n:.2f}")
    else:
        print("No processes to calculate.")

    #step 4: calculate context switches
    #I check the Gantt log to see how many times the running process changed
    if gantt_log is not None:
        context_switches = 0
        if len(gantt_log) > 0:
            prev_pid = gantt_log[0][2]
            for i in range(1, len(gantt_log)):
                current_pid = gantt_log[i][2]
                #if the PID changes from one block to the next, it's a switch
                if current_pid != prev_pid:
                    context_switches += 1
                    prev_pid = current_pid
        print(f"Total Context Switches:  {context_switches}")

def print_execution_log(processes, gantt_log):
    """
    this function prints a timeline of events: Arrivals, Starts, and Completions.
    it helps to see exactly what happened at each second.
    """
    print("\n" + "="*60)
    print("Execution Log")
    print("="*60)

    events = [] 
    #I use a priority system to order events happening at the same time:
    #1: Arrival 
    #2: Completion 
    #3: Start/Run 

    #1. log arrivals
    for p in processes:
        events.append((p.arrival_time, 1, f"{p.pid} arrives"))

    #2. log completions
    for p in processes:
        events.append((p.completion_time, 2, f"{p.pid} completes"))

    #3. log starts and preemptions
    gantt_log.sort(key=lambda x: x[0])
    
    for i, (start, end, pid) in enumerate(gantt_log):
        msg = f"{pid} starts running"
        
        #check if the previous process was preempted 
        if i > 0:
            prev_start, prev_end, prev_pid = gantt_log[i-1]
            if prev_end == start and prev_pid != pid:
                #find when the previous process actually finished
                prev_proc_completion = 0
                for p in processes:
                    if p.pid == prev_pid:
                        prev_proc_completion = p.completion_time
                        break
                
                #if it finished later than now, it means it was kicked out of CPU
                if prev_proc_completion > start:
                    msg += f" (preempts {prev_pid})"
        
        events.append((start, 3, msg))

    #sort all events by time
    events.sort(key=lambda x: (x[0], x[1]))

    #print events grouped by time (for example: t=0: P1 arrives, P1 starts running)
    for time, group in itertools.groupby(events, key=lambda x: x[0]):
        messages = [entry[2] for entry in group]
        print(f"t={time}: {', '.join(messages)}")
    
    print("\n")