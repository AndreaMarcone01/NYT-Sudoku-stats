# NYT-Sudoku-stats
Repository for stats of the NYT Sudoku that I started playing in 2026. 

## Scope
I want to have a good analysis of my plays, in particular how many plays, the average time for completing the puzzle, an histogram of my times and the evolution of my average time with more plays. 

## Contents
In the repository we found different files, this is a brief description of them. 
### times.txt
Text file with the times of the plays, divided in the three difficulty (easy, medium, hard). This file should be periodically updated. The format should *always* have the times of easy mode on row 3, for medium in row 5 and for hard in row 7 (in text editor the first line is 1, not 0). Better if the others lines start with the comment notation (#). The data are written in the `minutes:seconds` format and are separated by a comma.  
### analysis.py
Python file to run the analysis.
### README.dm
Obviously this readme.

## The analysis
At the start of the file we find two fundamentals functions: `string_to_sec` to convert from the time format of `minutes:seconds` to the much more easy to manipolate number of seconds and the opposite `sec_to_string` because the first format is prettier to see. 

Then we import the data from the `times.txt` file, the code and the comments should be self explanatory. At the end of import we have arrays with the three difficulties times. 

### Analysis: graph with evolution of mean and standard deviation
I wanted to see how my times impacted on the mean ($\mu$) and standard deviation ($\sigma$) and the evolution of these quantities with the grow of plays. 
To achieve this we use the `mean_and_std_series` function: given the array of seconds this finds $\mu$ and $\sigma$ after each new time. 