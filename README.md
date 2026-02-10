# NYT-Sudoku-stats
Repository for stats of the NYT Sudoku that I started playing in 2026. This is just a little side project but if you have some request try open an issue and I will try to respond :)

## Scope
I want to have a good analysis of my games, like how many games, the average time for completing the puzzle, an histogram of my times and the evolution of my average time with more plays. 

## How to use
Download the last release of the repository, then rewrite the `times.txt` file with yours games times. Then you can run `analysis.py` from your preferred python editor or from the terminal. It's necessary python with the packages: `os`, `numpy`, `pandas` and `matplotlib`. 

## Contents
In the repository we found different files, this is a brief description of them. 
### times.txt
Text file with the times of the plays, divided in the three difficulty (easy, medium, hard). This file should be periodically updated. The format should *always* have the times of easy mode on row 3, for medium in row 5 and for hard in row 7 (in text editor the first line is 1, not 0). Better if the others lines start with the comment notation (#). The data are written in the `minutes:seconds` format and are separated by a comma.  
### analysis.py
Python file to run the analysis.
### Easy/Medium/Hard_analysis.pdf
Files with the results of the analysis for the tree difficulties. 
### README.dm
Obviously this readme.

## The results
After running the analysis we have the files with the results. Inside this pdf file we find:
- In the top left some written statistic: number of games, mean time, best and worst time and in which game they are scored.
- In the top right we find an histogram of the game times. This is generated to have circa 16 bins.
- In the bottom we have a graph in which the dots are the game time, coloured in darker shade of red/green based on the difference with the mean. The mean is the blue line and the shaded area represent the one standard deviation interval.
The analysis is better described in the next section.

## The analysis
At the start of the file we find two fundamentals functions: `string_to_sec` to convert from the time format of `minutes:seconds` to the much more easy to manipolate number of seconds and the opposite `sec_to_string` because the first format is prettier to see. 

Then we import the data from the `times.txt` file, the code and the comments should be self explanatory. At the end of import we have arrays with the three difficulties times.

Here starts the real analysis with the three fundamentals functions: 
- `mean_and_std_series` function: I wanted to see how my game times impacted on the mean and standard deviation (std) and the evolution of these quantities with the grow of games. This function, given the array of seconds, finds mean and std after each new time. 
- `best_interval` this function finds the best interval to use to represent the data. The function has as inputs the array with game times in seconds and the number of intervals we want to have, the possible intervals are multiple of 15 seconds. 
- `analysis_plot` here the magic happens and we produce the final plot of the analysis. This function takes the times (in `mm:ss` format) and a string of the level of difficulty and saves in the directory of the `analysis.py` file the final plot.

These are the steps of `analysis_plot`

### Step 0: initialize
We convert the string times in seconds, we use `mean_and_std_series` and we define an array with the number of games. Then we initialize the plot: we will use the matplotlib `subplot2grid` graph ([matplotlib docs](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplot2grid.html)) and we define its shape to be `(3,5)` so 3 rows and 5 columns.

### Step 1: the text
The first subplot is the one in which we write as text some statistic of the game times. We define it to be in the top left corner (position with index `(0,0)`) and to span two columns. We then define the various string to print using the information of the difficulty string, the mean, the standard deviation and the best and worst times. We then plot them in a pretty way and we turn off the axis.

### Step 2: the histogram
The second subplot is the histogram of the game times. We define it to take the rest of the first row so in position with index `(0,2)` and to span three columns. Here we use `best_interval` to define the bins of the histogram, giving as the number of intervals 16. We then use matplotlib `hist` function to do the histogram and we fix the x and y axis to have the right label and ticks.

### Step 3: evolution of mean and standard deviation
The last subplot is the one with the evolution of the mean and std and will take all the remaining space so we use position with index `(1,0)` and we make it span 2 rows and 5 columns. Then we plot the mean as a line, using the numbers array for the x axis. We also use matplotlib's `fill_between` to shade the region of +/- 1 std around the mean, `alpha = 0.2` is used to add transparency. 
We then plot the single game times, and we specify the color to be the time minus the mean. Whit the right palette the color scheme will be darker red for games with time bigger then the mean and viceversa with green. 
The final touches are on the axis, with labels and ticks on the y axis using again `best_interval` with 8 as number of intervals, to have the closest interval to have 8 horizontal line in the graph.

### Step 4: save
Finally we save the image in the same directory of the `analysis.py` file. We also print a message to secure the user everything is okay.