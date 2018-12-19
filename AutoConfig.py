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
        if (re.search('^CHG. ',chg_or_inc) or re.search('^Chg.', chg_or_inc) or
            re.search('^chg.', chg_or_inc) or re.search('^INC.', chg_or_inc) or
            re.search('^Inc.', chg_or_inc) or re.search('^inc.', chg_or_inc)):
            if number_of-char !=13:
                print ('Please check change or incident number :')
                valid=False
            else:
                valid=True
        else:
             print ('Incorrect change or incident number or file name.  Please ensure file name as CHGXXXXXXXXXX.txt or INCXXXXXXXXXX.tst')
             valid=False
    return loginId, chg_or_inc, chg_or_inc+'.txt') 

def HostandConfigurationDict(file):
    configuration={}
    config_file=open(file,'r')
    flag=True
    for line in config_file:
        if '<' in line and '>' in line:
            if flag:
                ip_host=line.split('<')[1].split('>')
                ip_host.pop(1)
                flag=False
            else:
                print "Encounter consecuritve lines of <host,ip> in the change or the incident file.  Please seprate <host,ip> follow by clie command(s)"
                exit()
        else:
            flag=True
            key=ip_host[0].replace(',','/')
            try:
                configuration[key].append(line)
            except KeyError:
                configuration[key]=[line]
    config_file.close()
    return configuration

         
def LoginToDeviceForVerification(userId, conf_dict, type, chgId):
    host_ip_list=conf_dict.keys()
    file_dict={}
    for host_ip in host_ip_list:
        host=host_ip.split('/')[0]
        ip=host_ip.split('/')[1]
        telnet=telnetlib.Telnet(ip)
        telnet.read_until("login: ",3)
        if type =='pre':
            datatype='baseline configuration data'
         else:
            datatype='post configuration data'
            
         display(['Attempting to loing into',host,ip,'to capture', datatype],100]
         username=userId
         telnet.write(username +'/n')
         telnet.read_until("Password:")
         password=getpass.getpass()
         telnet.write(password +'/n')
         print "Attempting to authenticate"
    
    
    
    
    
