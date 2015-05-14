import numpy as np
import os, time
import os.path as path
import sys
import subprocess
import random
def parser():
    file = open('/home/michael/CUT_Drone/matlab_features/matlab_out', 'r')
    #print file.readline()
    
    first_line = file.readline()
    something = float(first_line)
    if int(something) == 1:
        s = file.readline()
    
        rows = s.split (',')
        rows= np.array(rows[:100])
        input_array = rows.astype(np.float)
        score = file.readline()
        score = float(score)
        file.close()
        for (x), value in np.ndenumerate(input_array):
            if(input_array[x]==1):
                input_array[x] = score
        return input_array,1,score
    else:
        result = np.zeros((100))
        
        return result,0,0

def softmax(x):
    x = np.exp(x)
    x = x / x.sum()
    return x
    
def reward_function(r0,score):
    if score==0:
        return -20
    elif score > 1.5:
        return 100
    elif score >= r0:
        return 1
    else:
        return -1
        
if __name__ == "__main__":  
    
    n_hidden= 10
    n_inputs= 100
    n_outputs = 8   
    n_steps = 30
    reward_vector = np.zeros((n_steps), dtype=np.int)
    input_vector = np.zeros((n_steps,n_inputs), dtype=np.float)
    path_to_watch = "/home/michael/CUT_Drone/matlab_features/matlab_out"
    first_time=path.getmtime(path_to_watch)
    temp = first_time
    h0 = np.zeros((n_hidden))
    r0 = 0;
    W = np.random.uniform(size=(n_hidden,n_hidden), low=-.01, high=.01)
    W_in = np.random.uniform(size=(n_inputs,n_hidden), low=-.01, high=.01)
    W_out = np.random.uniform(size=(n_hidden,n_outputs), low=-.01, high=.01)
    
    for i in range(0,n_steps):
        while 1:
            if temp!=first_time:
                time.sleep(2) # delays for 5 seconds
                x,flag,score=parser()
                input_vector[i,0:100] = x[:100]
                reward = reward_function(r0,score)
                r0 = score
                reward_vector[i]=reward
                if(reward==100):
                    break
                if flag==1:
                    h = np.dot(x,W_in) + np.dot(h0,W)
                    h = np.tanh(h)
                    y = np.dot(h,W_out)
                    y = softmax(y)
                
                    biggest = np.argmax(y)
                
                    h0=h
                else:
                    biggest = 7
                print "Sending command", i
                e=round(random.uniform(0.0, 1.0), 10)
                if e<0.5:
                    biggest=random.randint(0,7)
                subprocess.call(['/home/michael/CUT_Drone/scripts/publish_command_script.sh',`biggest`])  
                first_time=path.getmtime(path_to_watch)
                break
            else:
                temp = path.getmtime(path_to_watch)
        if reward==100:
            print "SUCCESS! Landing"
                subprocess.call(['/home/michael/CUT_Drone/scripts/publish_command_script.sh',`8`])  
    exp_name=input("The name of the experament:")
    np.savetxt('/home/michael/CUT_Drone/feed_forward_outputs/input_rcnn_features/'+str(exp_name)+'.txt', input_vector, fmt='%f')
    np.savetxt('/home/michael/CUT_Drone/feed_forward_outputs/rewards/'+str(exp_name)+'.txt', reward_vector, fmt='%d')
    #b = np.loadtxt('test1.txt', dtype=float)  this is how you load
    