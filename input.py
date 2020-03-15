from pynput import keyboard 
import csv, time
rep=0 #keeps a record of number of times the word is typed correctly
timing={} # records the up time , down time and hold time of the key
keys_logged=[] # keeps a record of the pressed key
rows=[] # it is a list of rows to be appended to csv file 
user_input='' #stores user input
pressed_keys='' # string of the keys pressed
n_input=1 # number of times to take input
on_press=[] #on key press we add key to this list and on key release we remove key from this list
is_capital_r=True #boolean condition to check if R is capital or small. b=True small r. b=False R(capital)
caps_lock_pressed=False #boolean condition to check if caps_lock is pressed or not
listener=0

def start_listener():
    global rows,listener
    global user_input,rep  
    with keyboard.Listener(on_press = call_press, on_release = call_release) as  listener1:
        listener=listener1
        listener1.join()
    print('rows ',rows)
    with open('test_data.csv', 'w') as file:
        output = csv.writer(file)
        output.writerows(rows)
    rows.clear()
        
def stop_listener():
    global rep,pressed_keys,on_press,is_capital_r
    pressed_keys=''
    is_capital_r=True
    on_press.clear()
    keys_logged.clear()
    timing.clear()
    caps_lock_pressed=False
    listener.stop()

def check_user_input():
    global rep,pressed_keys,is_capital_r, on_press
    if (pressed_keys!="'.''t''i''e''5'Key.shift_r'r''o''a''n''l'Key.enter" and pressed_keys!= "'.''t''i''e''5'Key.shift'r''o''a''n''l'Key.enter" and pressed_keys!="'.''t''i''e''5'Key.caps_lock'r'Key.caps_lock'o''a''n''l'Key.enter") or is_capital_r:
        pressed_keys=''
        is_capital_r=True
        on_press.clear()
        keys_logged.clear()
        timing.clear()
        caps_lock_pressed=False        
        return 
    rep+=1
    pressed_keys=''
    print('You have correctly typed ',rep,' time')
    # i and j are counters for while loop
    i=0
    j=1
    # row=[name,session,rep]
    row=[]
    if timing[keys_logged[5]]['up']<timing[keys_logged[6]]['up']:
        timing[keys_logged[5]]['up']=timing[keys_logged[6]]['up']
        timing[keys_logged[5]]['hold']=timing[keys_logged[5]]['up']-timing[keys_logged[5]]['down']    
    # for ii in timing:
    #     print(ii,timing[ii])     
    # print(k)
    while j<11:
        # print()
        row.append(timing[keys_logged[i]]['hold'])
        row.append(timing[keys_logged[j]]['down']-timing[keys_logged[i]]['down'])
        row.append(timing[keys_logged[j]]['down']-timing[keys_logged[i]]['up'])
        j+=1
        if j==6:
            j+=1
        i+=1
        if i==6:
            i+=1
    row.append(timing[keys_logged[i]]['hold'])
    timing.clear()
    keys_logged.clear()
    is_capital_r=True
    caps_lock_pressed=False
    on_press.clear()
    rows.append(row)
    
def call_release(key):
    global rep,timing,pressed_keys,caps_lock_pressed,on_press   
    user_input=time.time()
    try:
        on_press.remove(key)
        timing[key]['up']=user_input
        timing[key]['hold']=timing[key]['up']-timing[key]['down'] 
        # print(key,s) 
        if key==keyboard.Key.caps_lock:
            caps_lock_pressed=True
        if key==keyboard.Key.enter:        
            check_user_input()          
        if rep==1:
            rep=0
            return False  
    except ValueError: 
        pass
     
              
    
def call_press(key):
    global pressed_keys,is_capital_r,caps_lock_pressed, on_press
    pressed_keys+=str(key)
    if key!=keyboard.Key.shift and key!=keyboard.Key.shift_r and key!=keyboard.Key.caps_lock:
        keys_logged.append(key)
    if  hasattr(key,'char')  and key.char=='r':
        if keyboard.Key.shift in on_press or keyboard.Key.shift_r in on_press or caps_lock_pressed :
            is_capital_r=False
    on_press.append(key)
    global timing
    user_input=time.time()    
    if key not in timing:        
        timing[key]={}
    if 'down' not in timing[key]:
        timing[key]['down']=user_input