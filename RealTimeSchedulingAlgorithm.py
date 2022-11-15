# pandas: pip3 install pandas
# plotly: pip3 install plotly_express

import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import sys
import fileinput
import math

def handle_command_line_input():
    global processList
    global lowestCommon
    global numProcess

    count = 0
    processList = []
    lcmList = []

    with fileinput.input() as f:
        for line in f:
            process = []
            process = line.split(' ', 3)
            
            if count != 0:
                process[2] = process[2][:-1]
                for x in range(0,3):
                    process[x] = int(process[x])

                #Add time left attribute
                process.append(process[2])
                process.append(count)
                process.append(1)
                process.append(process[1])
                process.append(process[0])

                processList.append(process)
                lcmList.append(process[0])
            else:
                process[0] = process[0][:-1]
                numProcess = int(process[0])

            count = count + 1
    
    lowestCommon = LCMofArray(lcmList)
    
            
def calculate():
    processList.sort(key=lambda x: x[6])
    processList.sort(key=lambda x: x[5], reverse=True)
    currentTask = processList[0][4]
    cpuUtil = 0
    produceGanttChart = True
    alreadyProduced = False

    for i in range(numProcess):
        cpuUtil = cpuUtil + (processList[i][2] / processList[i][0])

        if(cpuUtil > 100):
            print("CPU utilization is greater than 100")
            produceGanttChart = False
            break
    
    listOfTasks = []

    time = 0
    prevTime = 0

    try:
        open('OutputFile.txt', 'w').close()
    except:
        return

    file = open('OutputFile.txt', 'w+')

    while(time < lowestCommon):
        processList.sort(key=lambda x: x[6])
        processList.sort(key=lambda x: x[5], reverse=True)
        
        if currentTask != processList[0][4]: 
            file.write(str(prevTime) + " - " + str(time) + ": Task " + str(currentTask) + "\n")

            listOfTasks.append(dict(Task="Task " + str(currentTask), Start=prevTime, Finish=time, Resource="Task " + str(currentTask), Times="Starts at: " + 
            str(prevTime) + ", Ends at: " + str(time)))

            currentTask = processList[0][4]
            prevTime = time

        # Remove one tick of time from the process that is running
        processList[0][3] = processList[0][3] - 1
        # Add one tick of time
        time = time + 1

        #Set up for next time
        if processList[0][3] == 0:
            processList[0][5] = 0

        for x in range(numProcess):
            #Check at deadline
            if processList[x][6] == time:
                if processList[x][5] == 1:
                    file.write("Task " + str(processList[x][4]) + " Failed at time " + str(time))

                    if(produceGanttChart):
                        alreadyProduced = True
                        df = pd.DataFrame(listOfTasks)

                        fig = ff.create_gantt(df, index_col='Resource', show_colorbar=True, group_tasks=True)
                        fig.update_layout(xaxis_type='linear')
                        fig.show()
                    break

            #Reset at period
            if processList[x][7] == time:
                processList[x][5] = 1
                processList[x][7] = processList[x][7] + processList[x][0]
                processList[x][3] = processList[x][2]
                processList[x][6] = time + processList[x][1]


    file.close()

    if produceGanttChart and not alreadyProduced:
        df = pd.DataFrame(listOfTasks)

        fig = ff.create_gantt(df, index_col='Resource', show_colorbar=True, group_tasks=True)
        fig.update_layout(xaxis_type='linear')
        fig.update_xaxes(tick0=0, dtick=20, ticks='inside', tickwidth=2, tickcolor='black')
        fig.show()

    return

def LCMofArray(a):
    lcm = a[0]
    for i in range(1,len(a)):
        lcm = lcm*a[i]//math.gcd(lcm, a[i])
    return lcm



def main():
    handle_command_line_input()
    calculate()

if __name__ == "__main__":
    main()
