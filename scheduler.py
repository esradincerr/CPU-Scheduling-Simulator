import argparse #import standard library. argparse is a python library that makes it easy to define and parse command line arguments.

#import utils's files
#parser: reads the text file and creates Process objects.
#gantt: draws the ASCII chart.
#statistics: prints the table and execution log.
from utils.parser import parse_input_file 
from utils.gantt import render_gantt_chart
from utils.statistics import print_stats, print_execution_log

#import scheduling algorithm functions
from algorithms.fcfs import solve_fcfs
from algorithms.sjf import solve_sjf
from algorithms.srtf import solve_srtf
from algorithms.rr import solve_rr
from algorithms.priority_np import solve_priority_np
from algorithms.priority_p import solve_priority_p

def main(): #main function to run the CPU scheduling simulator
    parser = argparse.ArgumentParser(description="CPU Scheduling Simulator") #define the arguments 
    parser.add_argument('--input', type=str, required=True, help="Path to input file")  # --input FILENAME: path to the process description file
    parser.add_argument('--algo', type=str, required=True, help="Algorithm: FCFS, SJF, SRTF, RR, PRIO_NP, PRIO_P") # --algo ALGO: one of FCFS, SJF, SRTF, RR, PRIO_NP, PRIO_P
    parser.add_argument('--quantum', type=int, help="Time quantum for RR") # --quantum Q: time quantum for RR (required if --algo RR)
    
    args = parser.parse_args() #parse the arguments provided by the user in the terminal

    # step 1: parse the input file
    processes = parse_input_file(args.input)
    if not processes: #if file is empty or not found, exit the program 
        return

    gantt_data = [] #prepare variables for the simulation
    algo_name = args.algo.upper() #convert input to uppercase(for example: 'rr'->'RR')

    print(f"\n--- {algo_name} Simulation Starting ---") #it takes the name of the algorithm that is currently running

    #step 2: run the selected algorithm based on user input
    if algo_name == 'FCFS':
        gantt_data = solve_fcfs(processes)
    elif algo_name == 'SJF':
        gantt_data = solve_sjf(processes)
    elif algo_name == 'SRTF':
        gantt_data = solve_srtf(processes)
    elif algo_name == 'RR': #RR requires a quantum value (ex: q=4)
        if args.quantum is None:
            print("Error: --quantum parameter is required for RR.")
            return
        gantt_data = solve_rr(processes, args.quantum)
    elif algo_name == 'PRIO_NP':
        gantt_data = solve_priority_np(processes)
    elif algo_name == 'PRIO_P':
        gantt_data = solve_priority_p(processes)
    else: #if the user typed an invalid algorithm name
        print(f"Error: Unknown algorithm '{algo_name}'")
        return
    
    #step3: display outputs
    render_gantt_chart(gantt_data) #program draw the ASCII gantt chart
    
    print_execution_log(processes, gantt_data)#program print the detailed execution log
    
    print_stats(processes, gantt_data) #program print the per process statistics table and context switches

if __name__ == "__main__":
    main()