import numpy as np
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

test = sec_to_string(np.array([61, 132]))
print(test)
test2 = string_to_sec(test)
print(test2)