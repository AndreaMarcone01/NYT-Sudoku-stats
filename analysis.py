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
    string = np.zeros(sec.size, dtype='<U5')
    # find minute and seconds
    mm = np.floor(sec/60).astype(int)
    ss = (sec - mm*60).astype(int)
    
    # combine minute and seconds in string
    # if we are working with a single number
    if string.size == 1:
        for ii in range(string.size):
            # add leading zero if needed
            if ss < 10:
                string = f"{mm}:0{ss}"
            else:
                string = f"{mm}:{ss}"
                
    # if we are working with an array
    else:
        for ii in range(string.size):
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

def best_interval(tt_sec, n_int):
    possible_intervals = np.arange(15, np.max(tt_sec), 15, dtype = int)
    interval = (np.max(tt_sec) - np.min(tt_sec))/n_int # we want 8 dashed lines in graph
    bool_array = np.abs(possible_intervals/interval -1) == np.min(np.abs(possible_intervals/interval -1)) # find best which of possible intervals are nearest to have 8 lines in graph 
    best = possible_intervals[bool_array].item()
    min = np.floor(np.min(tt_sec)/best) * best # min in best sec interval
    max = np.floor(np.max(tt_sec)/best + 1) * best # max in best sec interval
    ticks = np.arange(min, max+1, best)
    return min, max, ticks

def analysis_plot(tt_string, diff_string):
    tt_sec = string_to_sec(tt_string)
    means, stds = mean_and_std_series(tt_sec)
    numbers = np.arange(1, len(tt_sec)+1, 1)

    Data_plot = plt.figure(figsize = (7,6))
    shape = (3,5)
    # text box
    ax1 = plt.subplot2grid(shape=shape, loc=(0,0), colspan = 2)

    title_string = "NYT Sudoku analysis: "+diff_string
    number_string = "You played "+str(len(tt_sec))+" games"
    mean_string = "Mean time is "+sec_to_string(means[-1])+"$\\pm$"+sec_to_string(stds[-1])
    best_string = "Best time is "+sec_to_string(np.min(tt_sec))+"  (game "+str(numbers[tt_sec == np.min(tt_sec)].item())+")"
    worst_string = "Worst time is "+sec_to_string(np.max(tt_sec))+"  (game "+str(numbers[tt_sec == np.max(tt_sec)].item())+")"
    start = -0.25
    ax1.text(start, 0.95, s = title_string, weight = 'bold', color = 'royalblue', size = 12)
    ax1.text(start, 0.65, s = number_string)
    ax1.text(start, 0.4, s = mean_string)
    ax1.text(start, 0.15, s = best_string)
    ax1.text(start, -0.1, s = worst_string)
    ax1.axis('off')

    # histogram
    ax2 = plt.subplot2grid(shape=shape, loc=(0,2), colspan = 3)

    x_min, x_max, bins = best_interval(tt_sec, 16)
    ax2.hist(tt_sec, bins=bins, color = 'royalblue', rwidth=0.95)
    # better x axis
    ax2.set_xlabel('Game time')
    ax2.set_xlim([x_min-5, x_max+5])
    ax2.set_xticks(bins, labels = sec_to_string(bins), size = 'small', rotation = 45)
    # better y axis
    ax2.set_ylabel('Counts')

    # mean plot
    ax3 = plt.subplot2grid(shape=shape, loc=(1,0), colspan=5, rowspan=2)

    ax3.plot(numbers, means, label = 'Mean', color = 'darkblue', zorder = 1)
    ax3.fill_between(numbers, means-stds, means+stds, color = 'royalblue', alpha = 0.2, zorder = 1)
    ax3.scatter(numbers, tt_sec, alpha = 1, c=tt_sec-means, marker = 'o', label = 'Game time', cmap='RdYlGn_r', edgecolors = 'black', zorder = 2)
    # better x axis
    ax3.set_xlabel('Games played')
    ax3.set_xlim([0.75, np.max(numbers)+0.25])
    x_ticks = np.arange(1, len(tt_sec)+1, 2) # tick from 1 every 2 play 
    ax3.set_xticks(x_ticks, labels = x_ticks)
    # better y axis
    ax3.set_ylabel('Time')
    y_min, y_max, y_ticks = best_interval(tt_sec, 8)
    ax3.set_ylim([y_min-5, y_max+5])
    ax3.set_yticks(y_ticks, labels = sec_to_string(y_ticks))
    # grid, legend and save
    ax3.grid(linestyle='--', zorder = 0)
    ax3.legend()

    plt.tight_layout()
    print(main_dir+"\\"+diff_string+"_analysis.pdf")
    plt.savefig(main_dir+"\\"+diff_string+"_analysis.pdf")
    print(diff_string+": analysis completed!")

analysis_plot(t_e, "Easy")
analysis_plot(t_m, "Medium")
analysis_plot(t_h, "Hard")


test = string_to_sec(t_m)
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
y_min, y_max, y_ticks = best_interval(test, 8)
plt.ylim([y_min-5, y_max+5])
plt.yticks(y_ticks, labels = sec_to_string(y_ticks))

# grid, legend and save
plt.grid(linestyle='--', zorder = 0)
plt.legend()
plt.savefig(main_dir+"\\example_graph.pdf")
plt.close()

# work on the histogram 
test = string_to_sec(t_m)
means, stds = mean_and_std_series(test)
numbers = np.arange(1, len(test)+1, 1)
x_min, x_max, bins = best_interval(test, 16)
plt.hist(test, bins=bins, color = 'royalblue', rwidth=0.95)

# better x axis
plt.xlabel('Game time')
plt.xlim([x_min-5, x_max+5])
plt.xticks(bins, labels = sec_to_string(bins), size = 'small', rotation = 45)

# better y axis
plt.ylabel('Counts')
plt.close()

# work on the text box
test = string_to_sec(t_e)
means, stds = mean_and_std_series(test)
numbers = np.arange(1, len(test)+1, 1)

diff_string = "NYT Sudoku analysis: Easy"
number_string = "You played "+str(len(test))+" games"
mean_string = "Mean time \n"+sec_to_string(means[-1])+"$\\pm$"+sec_to_string(stds[-1])
best_string = "Best time is "+sec_to_string(np.min(test))+"  (game number "+str(numbers[test == np.min(test)].item())+")"
worst_string = "Worst time is "+sec_to_string(np.max(test))+"  (game number "+str(numbers[test == np.max(test)].item())+")"
plt.text(0.5,0.75,s = diff_string, horizontalalignment = 'center')
plt.text(0.5,0.65,s = number_string, horizontalalignment = 'center')
plt.text(0.5,0.5,s = mean_string, horizontalalignment = 'center', linespacing = 1.5)
plt.text(0.5,0.4,s = best_string, horizontalalignment = 'center', linespacing = 1.5)
plt.text(0.5,0.3,s = worst_string, horizontalalignment = 'center', linespacing = 1.5)
plt.close()

# then we have to combine them in a single file
test = string_to_sec(t_m)
means, stds = mean_and_std_series(test)
numbers = np.arange(1, len(test)+1, 1)

fig = plt.figure(figsize = (7,6))
shape = (3,5)
# text box
ax1 = plt.subplot2grid(shape=shape, loc=(0,0), colspan = 2)

diff_string = "NYT Sudoku analysis: Medium"
number_string = "You played "+str(len(test))+" games"
mean_string = "Mean time is "+sec_to_string(means[-1])+"$\\pm$"+sec_to_string(stds[-1])
best_string = "Best time is "+sec_to_string(np.min(test))+"  (game "+str(numbers[test == np.min(test)].item())+")"
worst_string = "Worst time is "+sec_to_string(np.max(test))+"  (game "+str(numbers[test == np.max(test)].item())+")"
start = -0.25
ax1.text(start, 0.95, s = diff_string, weight = 'bold', color = 'royalblue', size = 12)
ax1.text(start, 0.65, s = number_string)
ax1.text(start, 0.4, s = mean_string)
ax1.text(start, 0.15, s = best_string)
ax1.text(start, -0.1, s = worst_string)
ax1.axis('off')

# histogram
ax2 = plt.subplot2grid(shape=shape, loc=(0,2), colspan = 3)

x_min, x_max, bins = best_interval(test, 16)
ax2.hist(test, bins=bins, color = 'royalblue', rwidth=0.95)
# better x axis
ax2.set_xlabel('Game time')
ax2.set_xlim([x_min-5, x_max+5])
ax2.set_xticks(bins, labels = sec_to_string(bins), size = 'small', rotation = 45)
# better y axis
ax2.set_ylabel('Counts')

# mean plot
ax3 = plt.subplot2grid(shape=shape, loc=(1,0), colspan=5, rowspan=2)

ax3.plot(numbers, means, label = 'Mean', color = 'darkblue', zorder = 1)
ax3.fill_between(numbers, means-stds, means+stds, color = 'royalblue', alpha = 0.2, zorder = 1)
ax3.scatter(numbers, test, alpha = 1, c=test-means, marker = 'o', label = 'Game time', cmap='RdYlGn_r', edgecolors = 'black', zorder = 2)
# better x axis
ax3.set_xlabel('Games played')
ax3.set_xlim([0.75, np.max(numbers)+0.25])
x_ticks = np.arange(1, len(test)+1, 2) # tick from 1 every 2 play 
ax3.set_xticks(x_ticks, labels = x_ticks)
# better y axis
ax3.set_ylabel('Time')
y_min, y_max, y_ticks = best_interval(test, 8)
ax3.set_ylim([y_min-5, y_max+5])
ax3.set_yticks(y_ticks, labels = sec_to_string(y_ticks))
# grid, legend and save
ax3.grid(linestyle='--', zorder = 0)
ax3.legend()

plt.tight_layout()
plt.savefig(main_dir+"\\test_analysis.pdf")