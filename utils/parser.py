class Process: 
    """""
    represents a single process in the simulation.
    this class holds all the timing data (arrival, burst) and 
    the final calculated statistics (waiting, turnaround, etc.)
    """""
    def __init__(self, pid, arrival_time, burst_time, priority):
        #basic information from the input file
        self.pid = pid
        self.arrival_time = int(arrival_time)
        self.burst_time = int(burst_time)
        self.priority = int(priority)

        self.remaining_time = self.burst_time #remaining_time equal to the total burst time

        #these variables will store our simulation results
        self.start_time = -1       #time when the CPU first starts this process
        self.completion_time = 0   #time when the process finishes execution
        self.waiting_time = 0      #total time spent waiting in the ready queue
        self.turnaround_time = 0   #total time from arrival to completion
        self.response_time = 0     #time from arrival to the first CPU attention

    def __repr__(self): #this function helps print the process object nicely for debugging
        return f"Process(PID={self.pid}, Arr={self.arrival_time}, Burst={self.burst_time}, Prio={self.priority})"

def parse_input_file(filename):
    """
    this function reads the 'processes.txt' file line by line.
    it ignores comments and empty lines to prevent errors.
    """
    processes = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()

                #step 1: skip lines that are empty or start with '#' 
                if not line or line.startswith('#'):
                    continue

                #step 2: split the line into parts based on spaces
                parts = line.split()

                #we expect exactly 4 columns: PID, Arrival, Burst, Priority
                if len(parts) >= 4:
                    pid = parts[0]
                    arrival = parts[1]
                    burst = parts[2]
                    priority = parts[3]

                    #create a new process object and add it to our list
                    processes.append(Process(pid, arrival, burst, priority))

        #step 3: sort the processes by arrival time
        #this is crucial because almost all algorithms assume processes come in order            
        processes.sort(key=lambda x: x.arrival_time)

        return processes
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []