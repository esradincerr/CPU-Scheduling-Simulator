import matplotlib.pyplot as plt
import copy
import sys
import io
import contextlib
from utils.parser import parse_input_file
#importing all algorithms to run them in a loop
from algorithms.fcfs import solve_fcfs
from algorithms.sjf import solve_sjf
from algorithms.srtf import solve_srtf
from algorithms.rr import solve_rr
from algorithms.priority_np import solve_priority_np
from algorithms.priority_p import solve_priority_p

def calculate_stats(processes, gantt_log):
    """
    helper function to calculate the average waiting, turnaround, and response times
    it calculates the metrics needed for the comparison table
    """
    n = len(processes)
    if n == 0: return 0, 0, 0, 0

    #calculating the averages by summing up individual stats and dividing by n
    avg_wait = sum(p.waiting_time for p in processes) / n
    avg_wait = sum(p.waiting_time for p in processes) / n
    avg_turn = sum(p.turnaround_time for p in processes) / n
    avg_resp = sum(p.response_time for p in processes) / n
    
    #calculate context switches by checking changes in PID
    context_switches = 0
    if gantt_log:
        prev_pid = gantt_log[0][2]
        for i in range(1, len(gantt_log)):
            current_pid = gantt_log[i][2]
            #if the pid is different from the previous one, it means a switch happened
            if current_pid != prev_pid:
                context_switches += 1
                prev_pid = current_pid
                
    return avg_turn, avg_wait, avg_resp, context_switches

def main():
    #first i read the processes from the input file
    filename = "processes.txt"
    original_processes = parse_input_file(filename)
    
    #checking if the file was read correctly
    if not original_processes:
        print(f"Error: {filename} not found.")
        return
    
    #listing all the algorithms i implemented to loop through them easily
    algorithms = [
        ("FCFS", solve_fcfs, False),
        ("SJF", solve_sjf, False),
        ("SRTF", solve_srtf, False),
        ("RR(q=4)", solve_rr, True), #round robin needs the quantum parameter
        ("PRIO_NP", solve_priority_np, False),
        ("PRIO_P", solve_priority_p, False)
    ]
    
    #this dictionary will hold the results to create graphs later
    results = {
        "names": [],
        "avg_waiting": [],
        "avg_turnaround": []
    }
    
    #defining column widths
    w_alg = 12
    w_turn = 18
    w_wait = 15
    w_resp = 16
    w_ctx = 18
    
    #printing the table header
    print("\n" + "-" * 85)
    header = f"{'Algorithm':<{w_alg}} {'Avg. Turnaround':<{w_turn}} {'Avg. Waiting':<{w_wait}} {'Avg. Response':<{w_resp}} {'Context Switches':<{w_ctx}}"
    print(header)
    print("-" * 85)
    
    #now i loop through each algorithm to run simulations
    for name, func, needs_quantum in algorithms:
        #I use deepcopy so that one algorithm doesn't mess up the data for the next one
        procs = copy.deepcopy(original_processes)
        
        #I suppress the output (Gantt charts) here to keep the table clean
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            if needs_quantum:
                gantt_data = func(procs, quantum=4)
            else:
                gantt_data = func(procs)

        #calculating the stats for the current run    
        avg_turn, avg_wait, avg_resp, ctx_switches = calculate_stats(procs, gantt_data)

        #saving the results for the graphs
        results["names"].append(name)
        results["avg_waiting"].append(avg_wait)
        results["avg_turnaround"].append(avg_turn)
        
        #printing the results row formatted nicely with 2 decimal places
        row = f"{name:<{w_alg}} {avg_turn:<{w_turn}.2f} {avg_wait:<{w_wait}.2f} {avg_resp:<{w_resp}.2f} {ctx_switches:<{w_ctx}}"
        print(row)

    print("-" * 85)
    #finally, creating the graphs based on the results
    create_graphs(results)

def create_graphs(results):
    names = results["names"]
    
    #creating the first bar chart for average waiting time
    plt.figure(figsize=(10, 6))
    plt.bar(names, results["avg_waiting"], color='skyblue', edgecolor='black')
    plt.xlabel("Algorithm")
    plt.ylabel("Average Waiting Time (ms)")
    plt.title("Average Waiting Time vs Algorithm")
    plt.grid(axis='y', linestyle='--', alpha=0.5)

    #saving the plot as an image file
    plt.savefig("avg_waiting.png")
    
    #creating the second bar chart for average turnaround time
    plt.figure(figsize=(10, 6))
    plt.bar(names, results["avg_turnaround"], color='salmon', edgecolor='black')
    plt.xlabel("Algorithm")
    plt.ylabel("Average Turnaround Time (ms)")
    plt.title("Average Turnaround Time vs Algorithm")
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.savefig("avg_turnaround.png")

if __name__ == "__main__":
    main()