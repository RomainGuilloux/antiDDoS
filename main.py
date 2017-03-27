#Author : Vinay Chandran
#Project : RadPRO
#Date : 27 March 2017

#packages
import time
import os
import subprocess
from threading import Thread

def init():
    print 'Starting RadPRO'
    time.sleep(0.4)

#regex to find IPs from file: (25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)

def term_command(command):
    term_output=subprocess.Popen('%s'%command, shell=True, stdout=subprocess.PIPE, )
    term_output=term_output.communicate()[0]
    return term_output

def check_os():
    print 'Checking OS'
    time.sleep(0.4)
    os_check_op=term_command('uname -s')
    if 'Darwin' in os_check_op:
        os_found='Mac'
        print 'Mac OS Detected'
    elif 'Linux' in os_check_op:
        os_found='Linux'
        print 'Linux Detected'
    else:
        os_found='Other'
        print 'Non UNIX Detected'
    time.sleep(0.4)
    return os_found

def find_ip(os_found):
    #finds IP of the current system
    print 'Finding local IP'
    time.sleep(0.4)
    if 'Mac' in os_found:
        loopback_ip=term_command('ipconfig getifaddr en0')
    else:
        loopback_ip=term_command('hostname -I')
    print 'IP Found : %s'%loopback_ip
    return loopback_ip

def check_log():
    #fetches IPs from the log and excludes local IP
    log_ips=term_command("grep -o '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' 1.log | grep -v %s"%loopback_ip)
    #filter removes blanks, split is used to create array from lines
    log_array=filter(None, log_ips.split('\n'))
    log_uniq=list(set(log_array))
    for i in log_uniq:
        count=log_array.count(i)
        print '%s'%i +' : %d'%count
        if count>100:
            print '\tBlacklisting %s' %i
            term_command('echo %s > ban_list.txt'%i)

def display_iptable():
    disp_op=term_command('sudo iptables -L')
    print disp_op

def ban_ip(ip_to_block):
    block_op=term_command('sudo iptables -I INPUT -s %s -j REJECT' %ip_to_block)
    print block_op

def unblock_ip(ip_to_unblock):
    unblock_op=term_command('sudo iptables -D INPUT -s %s -j REJECT' %ip_to_unblock)
    print unblock_op

def whitelist_ip(whitelist):
    allow_ip=term_command('sudo iptables -I INPUT -s %s -j ALLOW' %whitelist)
    print allow_ip

# def clear_log():

init()

os_found=check_os()

loopback_ip=find_ip(os_found)

check_log()
