import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Function to turn the string in format mm:ss to a integer of seconds
def string_to_sec(string):
    # initialize sec
    sec = np.zeros(len(string), dtype = int)

    # split the string, transform to inter and multiply to have seconds
    for ii in range(len(sec)):
        mm, ss = string[ii].split(':')
        sec[ii] = int(mm)*60 + int(ss)
    
    return sec

# Inverse function to turn the integrer of seconds to a string in format mm:ss
def sec_to_string(sec):
    # initialize string
    string = np.zeros(len(sec), dtype='<U5')
    # find minute and seconds
    mm = np.floor(sec/60).astype(int)
    ss = (sec - mm*60).astype(int)

    # combine minute and seconds in string
    for ii in range(len(string)):
        # add leading zero if needed
        if ss[ii] < 10:
            string[ii] = f"{mm[ii]}:0{ss[ii]}"
        else:
            string[ii] = f"{mm[ii]}:{ss[ii]}"

    return string


# Import the data
main_dir = os.path.dirname(os.path.realpath(__file__)) # directory of the file
data = pd.read_csv(main_dir+"\\times.txt", sep = '|', skiprows = [1,3,5]) # import as panda dataframe, skiprows header and difficulty comments 

# separe the 3 difficulties
easy = data.iloc[0]
medium = data.iloc[1]
hard = data.iloc[2]

# from row of dataframe to array in which every time is an element 
t_e = easy.str.split(',').iloc[0]
t_m = medium.str.split(',').iloc[0]
t_h = hard.str.split(',').iloc[0]

# Let's start the analysis
# Define a function that given the array of seconds finds the mean and std and their evolution
def mean_and_std_series(tt_sec):
    length = len(tt_sec)
    # initialize vectors
    mean_series = np.zeros(length)
    std_series = np.zeros(length)

    mean_series[0] = tt_sec[0]
    for ii in range(1,length):
        mean_series[ii] = np.mean(tt_sec[:ii+1])
        std_series[ii] = np.std(tt_sec[:ii+1])

    return mean_series, std_series

test = string_to_sec(t_e)
means, stds = mean_and_std_series(test)
numbers = np.arange(1, len(test)+1, 1)

# Graph the data: mean and 1 sigma interval, times colored based on how good is the time in respect of mean
plt.plot(numbers, means, label = 'Mean', color = 'darkblue', zorder = 1)
plt.fill_between(numbers, means-stds, means+stds, color = 'royalblue', alpha = 0.2, zorder = 1)
plt.scatter(numbers, test, alpha = 1, c=test-means, marker = 'o', label = 'Game time', cmap='RdYlGn_r', edgecolors = 'black', zorder = 2)

# better x axis
plt.xlabel('Games played')
plt.xlim([0.75, np.max(numbers)+0.25])
x_ticks = np.arange(1, len(test)+1, 2) # tick from 1 every 2 play 
plt.xticks(x_ticks, labels = x_ticks)

# better y axis
plt.ylabel('Time')
y_min = np.floor(np.min(test)/30) * 30 # min in 30 sec interval
y_max = np.floor(np.max(test)/30 + 1) * 30 # max in 30 sec interval
plt.ylim([y_min-5, y_max+5])
y_ticks = np.arange(y_min, y_max+1, 30)
plt.yticks(y_ticks, labels = sec_to_string(y_ticks))

# grid, legend and save
plt.grid(linestyle='--', zorder = 0)
plt.legend()
plt.savefig(main_dir+"\\example_graph.pdf")
plt.show()
