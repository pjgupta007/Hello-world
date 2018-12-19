import os
import telenetlib
import getpass
import socket
import re
import time 
import difflib
cli_list=['term len 0', 'show clock', 'show run', 'show ip route', 'show int status', 'show cdp neigh']

def validate_ip(s):
    a=s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i=int(x)
        if i<0 or i > 255:
             return False
    return True
    
   
def GetHostUserPass():
    hostname=True
    ipaddr=validate_ip('1.1.1.1')
    while hostname and ipaddr:
        try:
           host=raw_input('Enter hostname or ip address of the host:  ')
           if validate_ip(host):
               host=host
               hostname=False
               ipaddr=True
           else:
               host_addr=socket.gethostbyname(host)
               hostname=True
               ipaddr=False
        except socket.gaierror:
              print ('Host not found')
              hostname=True
    user=raw_input('Enter user name:  ')
    passwd=getpass.getpass()
    return host, user, passwd
    
def GetChangeorIncidentFile():
    valid=False
    loginId=raw_input('Enter username or ID:  ')
    while not valid:
        config_file=raw_input('Enter change or incident configuration file:  ')
        chg_or_inc=config_file.split('.')[0]
        number_of_char=len(chg_or_inc)
        if (re.search('^CHG. ',chg_or_inc) or re.search
         
