#Author : Vinay Chandran
#Project : RadPRO
#Date : 27 March 2017

#packages
import datetime
import time
import os
import sys
import subprocess
from threading import Thread
from time import strftime

blacklist_table=[]
var_limit=25
def log_it(logtext):
    term_command('echo %s >> log.txt'%logtext)
def loadanim():
    for i in range(4):
        time.sleep(0.2)
        sys.stdout.write('.')
        sys.stdout.flush()
    sys.stdout.write('\n')
def init():
    os.system('cls' if os.name == 'nt' else "printf '\033c'")
    print ('Starting RadPRO'),
    loadanim()
    time.sleep(0.1)

def term_command(command):
    term_output=subprocess.Popen('%s'%command, shell=True, stdout=subprocess.PIPE, )
    term_output=term_output.communicate()[0]
    return term_output

def check_os():
    print 'Checking OS',
    loadanim()
    time.sleep(0.1)
    os_check_op=term_command('uname -s')
    if 'Darwin' in os_check_op:
        os_found='Mac'
        print 'Mac OS Detected\n'
    elif 'Linux' in os_check_op:
        os_found='Linux'
        print 'Linux OS Detected\n'
    else:
        os_found='Other'
        print 'Non UNIX Detected'
    time.sleep(0.4)
    return os_found

def find_ip(os_found):
    #finds IP of the current system
    print 'Finding local IP',
    loadanim()
    time.sleep(0.1)
    if 'Mac' in os_found:
        loopback_ip=term_command('ipconfig getifaddr en0')
    else:
        loopback_ip=term_command('hostname -I')
    loopback_ip=loopback_ip.split()[0]
    print 'IP Found : %s'%loopback_ip
    cur_time=strftime("%Y-%m-%d %H:%M:%S")
    logger='New iteration at : %s' %cur_time + ' on %s' %loopback_ip
    term_command('echo %s >> log.txt'%logger)
    return loopback_ip

def get_vars():
    var_limit=25
    exit_var=1
    while(exit_var==1):
        choice=(raw_input('Use the defaults for maximum connection requests? (Y/N):')).lower()
        if choice == 'y':
            exit_var=0
        elif choice == 'n':
            exit_var=0
            opt=(raw_input('Choose : \n1) Home PC (10)\n2) Small Scale Enterprise (20)\n3) Large Enterprise(40)\n4) Custom\n'))
            if opt == '1':
                var_limit=10
            elif opt == '2':
                var_limit=20
            elif opt == '3':
                var_limit=40
            elif opt == '4':
                try:
                    var_limit=int(raw_input('Enter the custom value : '))
                except ValueError:
                    print('Not a valid number')
                    exit_var=1
        else :
            print 'Invalid choice.'
    print 'Using %s as connection limit'%var_limit

def darth(ip):
    finder=-1
    for i in blacklist_table:
        if ip in i:
            finder= blacklist_table.index(i)
    if (finder==-1):
        print ('%s not in BlackList Table.. Adding it!'%ip)
        now= datetime.datetime.now()
        timeout= now + datetime.timedelta(minutes = 15)
        temparray=[ip,1,1,now]
        blacklist_table.append(temparray)
        ban_ip(ip)
    elif(finder!=-1):
        print ('%s found in BlackList history. Increasing timeout!'%ip)
        blacklist_table[finder][1]=1
        blacklist_table[finder][2]+=1
        now= datetime.datetime.now()
        timeout=blacklist_table[finder][3]
        if timeout < now:
            timeout=now + datetime.timedelta(minutes = 5*blacklist_table[finder][2])
        if timeout > now:
            timeout=timeout + datetime.timedelta(minutes = 5*blacklist_table[finder][2])
        blacklist_table[finder][3]=timeout

def release_manager():
    for i in blacklist_table:
        if i[3] > now:
            blacklist_table[1]=0
            Print ("Releasing %s"%i[0])
            release_ip(i[0])

def check_log():
    #fetches IPs from the log and excludes local IP
    print 'Loading log',
    loadanim()
    log_ips=term_command("grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' 1.log | grep -v %s"%loopback_ip)
    #filter removes blanks, split is used to create array from lines
    log_array=filter(None, log_ips.split('\n'))
    log_uniq=list(set(log_array))
    print 'Log Extracted'
    #Clearing the log
    open('1.log', 'w').close()
    print 'Old log deleted'
    for index,i in enumerate(log_uniq):
        count=log_array.count(i)
        into_csv='%d,'%index+'%s'%i+',%i'%count+'\n'
        term_command('echo %s >> table.csv'%into_csv)
        print into_csv
        if count>var_limit:
            print '\tBlacklisting %s' %i
            cur_time=strftime("%Y-%m-%d %H:%M:%S")
            log_it('%s'%cur_time+'\t Blacklisted %s'%i)
            darth(ip)
            term_command('echo %s >> ban_list.txt'%i)

def display_iptable():
    print '\n\nDisplaying current IPTable Values\n\n'
    disp_op=term_command('sudo iptables -L')
    print disp_op
    print '\n\n'

def ban_ip(ip_to_block):
    block_op=term_command('sudo iptables -I INPUT -s %s -j REJECT' %ip_to_block)
    print block_op

def release_ip(ip_to_unblock):
    unblock_op=term_command('sudo iptables -D INPUT -s %s -j REJECT' %ip_to_unblock)
    print unblock_op

def whitelist_ip(whitelist):
    allow_ip=term_command('sudo iptables -I INPUT -s %s -j ALLOW' %whitelist)
    print allow_ip

# def clear_log():

init()
os_found=check_os()
loopback_ip=find_ip(os_found)
get_vars()
display_iptable()

while True:
    check_log()
    time.sleep(3)
    os.system('cls' if os.name == 'nt' else "printf '\033c'")
    print("Running Release Manager")
    release_manager()
