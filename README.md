# CPU Process Scheduling Simulator

**Name:** Esra Dinçer
**Department:** Computer Engineering 

## 1. Project Overview
This project implements a CPU Process Scheduling Simulator in Python 3. The simulator supports multiple classical scheduling algorithms to demonstrate how an Operating System manages process execution. It parses a process input file, simulates the execution logic, generates ASCII Gantt charts, calculates detailed per-process statistics (Turnaround, Waiting, Response times), and provides a comparative analysis of different algorithms using graphs.

## 2. Dependencies and Setup
* **Python Version:** Python 3
* **External Libraries:** `matplotlib` (Used for generating comparison graphs).
* **Standard Libraries:** `argparse`, `copy`, `sys`, `io`, `contextlib`.

To install the required library, run:
```bash
pip install matplotlib
```
## 3. Project Structure
The project is organized in a modular structure:

scheduler_project/
├── scheduler.py        *** Main script for single algorithm simulation
├── compare.py          *** Script to compare all algorithms and generate graphs
├── processes.txt       *** Input data file
├── README.md           *** Project documentation
├── avg_waiting.png     *** Graph output from compare.py
├── avg_turnaround.png  *** Graph output from compare.py
├── utils/
│   ├── parser.py       *** Handles file parsing and Process class definition
│   ├── gantt.py        *** Renders the ASCII Gantt chart
│   └── statistics.py   *** Handles calculation and printing of statistics tables
└── algorithms/
    ├── fcfs.py         *** First-Come First-Served implementation
    ├── sjf.py          *** Shortest Job First implementation
    ├── srtf.py         *** Shortest Remaining Time First implementation
    ├── rr.py           *** Round Robin implementation
    ├── priority_np.py  *** Non-Preemptive Priority implementation
    └── priority_p.py   *** Preemptive Priority implementation

## 4. How to Run the Simulator

A. Running a Specific Algorithm:
You can use scheduler.py to simulate a single algorithm and see the Gantt chart and detailed statistics.

Syntax:
python scheduler.py --input processes.txt --algo [ALGO_NAME] --quantum [VALUE]

Supported Algorithms:
--FCFS
--SJF
--SRTF
--RR (Requires -- time quantum)
--PRIO_NP
--PRIO_P

Sample Commands:
  1.Run First-Come First-Served implementation:
python scheduler.py --input processes.txt --algo FCFS

  2.Run Shortest Job First implementation:
python scheduler.py --input processes.txt --algo SJF

  3.Run Shortest Remaining Time First implementation:
python scheduler.py --input processes.txt --algo SRTF  

  4.Run Round Robin (with Quantum = 4):
python scheduler.py --input processes.txt --algo RR --quantum 4
 
  5.Non-Preemptive Priority implementation:
python scheduler.py --input processes.txt --algo PRIO_NP  
  
  6.Run Preemptive Priority:
python scheduler.py --input processes.txt --algo PRIO_P

B. Running the Comparison Script:
To run all algorithms consecutively, generate a summary table, and create performance graphs:
python compare.py

Output: A formatted table in the terminal showing Average Turnaround, Waiting, Response times, and Context Switch counts.

Graphs: Two image files (avg_waiting.png and avg_turnaround.png) will be created in the project directory.

## 5. Algorithm Implementations
FCFS (First-Come First-Served): * Logic: Processes are executed strictly in the order of their arrival time.
  --Type: Non-preemptive.

SJF (Shortest Job First): * Logic: The process with the smallest burst time in the ready queue is selected next.
  --Type: Non-preemptive.

SRTF (Shortest Remaining Time First): * Logic: A preemptive version of SJF. If a new process arrives with a remaining time shorter than the current running process, the CPU switches to the new process.
  --Type: Preemptive.

Round Robin (RR): * Logic: Each process is assigned a fixed time unit (Quantum). If the process does not finish within this time, it is moved to the back of the ready queue.
  --Type: Preemptive.

Priority (Non-Preemptive): * Logic: Processes are selected based on priority value (lower number = higher priority). Once a process starts, it runs until completion.
   --Type: Non-preemptive.

Priority (Preemptive): * Logic: Similar to non-preemptive priority, but if a process with higher priority arrives, the currently running process is interrupted.
  --Type: Preemptive.

## 6. Input File Format
The input file (processes.txt) uses the following format (lines starting with # are ignored):

# pid arrival_time burst_time priority
P1    0            8          2
P2    1            4          1 
P3    2            9          3
P4    3            5          2

## 7. Discussion of Results
Based on the simulations performed on the test data:
    Best Performance (Waiting/Turnaround Time): SRTF generally yielded the lowest average waiting and turnaround times. This is expected because SRTF always processes the task closest to completion, minimizing the time other processes wait.
    
    Response Time: Round Robin provided the best (lowest) average response time. By giving every process a small slice of CPU time quickly, it ensures no process waits too long to start, making it ideal for interactive systems.

    Context Switches: Preemptive algorithms like RR, SRTF, and PRIO_P resulted in a significantly higher number of context switches compared to non-preemptive ones (FCFS, SJF). While preemption improves responsiveness, the high context switch count indicates a higher system overhead.

    Surprising Behavior: In FCFS, if a long process arrives first (like P1 with burst 8), it delays all subsequent shorter processes significantly (Convoy Effect). In contrast, SJF rearranged the execution order completely to P1 -> P2 -> P4 -> P3, drastically reducing the waiting time for P2 and P4.