import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# function to turn the string in format mm:ss to a integer of seconds
def string_to_sec(string):
    # initialize sec
    sec = np.zeros(len(string), dtype = int)

    # split the string, transform to inter and multiply to have seconds
    for ii in range(len(sec)):
        mm, ss = string[ii].split(':')
        sec[ii] = int(mm)*60 + int(ss)
    
    return sec

# inverse function to turn the integrer of seconds to a string in format mm:ss
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


# import the data
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

# let's start the analysis
# define a function that given the array of seconds finds the mean and std and their evolution
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
print(test)
print(np.mean(test))
print(means)
print(stds)

numbers = np.arange(1, len(test)+1, 1)
plt.plot(numbers, test, '.', label = 'Times of plays')
plt.plot(numbers, means, label = 'Means')
plt.plot(numbers, means+stds, '--', label = 'Means+std')
plt.plot(numbers, means-stds, '--', label = 'Means-std')
plt.xlabel('Number of plays')
plt.ylabel('Time [s]')
plt.legend()
plt.show()