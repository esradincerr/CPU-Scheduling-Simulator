def render_gantt_chart(gantt_log):
    """
    this function draws a text based (ASCII) gantt chart on the terminal
    it visualizes which process is running at what time
    """
    if not gantt_log:
        return

    print("\n" + "="*50)
    print("ASCII Gantt Chart")
    print("="*50)

    #step 1: draw the top border
    #for every entry in the log, I add a box segment "+-------"
    upper_line = ""
    for _ in gantt_log:
        upper_line += "+-------"
    upper_line += "+"
    print(upper_line)

    #step 2: draw the Process IDs ---
    #I place the process ID (like P1, P2) in the middle of each box
    pid_line = ""
    for entry in gantt_log:
        pid = entry[2]
        #I use formatting {pid:<3} to make sure it looks neat even if PID is short
        pid_line += f"|  {pid:<3}  "
    pid_line += "|"
    print(pid_line)

    #step 3: draw the Bottom Border ---
    #this is exactly the same as the top border
    print(upper_line)

    #step 4: draw the Timeline (Numbers) ---
    #this loop aligns the time numbers exactly under the '+' signs
    time_line = f"{gantt_log[0][0]}" #start time 
    
    for entry in gantt_log:
        end_time = entry[1]
        
        #calculate how many spaces I need to align the next number properly
        space_count = 8 - len(str(end_time))
        if space_count < 1: space_count = 1
        
        time_line += " " * space_count + str(end_time)
        
    print(time_line)
    print("\n")