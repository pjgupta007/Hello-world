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
         for cli in cli_list:
                 telnet.write(cli+'\n')
                 time.sleep(5)
                 print"******* proccessing request, please standby ************'
                 time.sleep(3)
          telnet.write('exit'+'\n')
          output_data=telnet.read_all()
          filename=host+'_'+type+'.'+chgId
          file_dict[host]=filename
          file=open(filename,'w')
          file.write(output_data)
          file.close()
    return file_dict
    
def Configuration(Config_dict,userID,chgId):
     config_file_list=[]
     for key in config_dict.key():
         host=key.split('/')[0]
         ip=key.split('/')[1]
         password=getpass.getpass()
         telnet=telnetlib.Telnet(ip)
         telnet.read_until('login:',3)
         display([' Attempting to login into' ,host,ip,'for configuration'],100)
         username=userID
         telnet.write(username +'\n')
         if password:
              telnet.read_unitl('assword:')
              telnet.write(password +'\n')
          telnet.read_until('#', 3)
          print 'Attempting to authenticate '
          for config_line in config_dict[key]:
               if '[' in config_line and ']' in config line and 'command_start' in config_line:
                    config_line='config t'
                    telnet.write(config_line +'\n')
                    time.sleep(5)
                elif '[' in config_line and ']' in config_line and 'command_end' in config_line:
                     config_line='end \n'
                     telnet.write(config_line)
                     sleep.time(3)
                     telnet.write('exit \n')
                     sleep.time(3)
                     output=telnet.read_all()
                     output_dump_file=host+'_config'+'.'+chgId
                     dump_file=open(output_dump_file,'w')
                     dump_file.write(output)
                     dump_file.close()
                     config_file_list.append(output_dump_file)
                  else:
                     time.sleep(1)
                     telnet.write(config_line)
                     time.sleep(2)
                
def compare(dict1, dict2):
    diff_file_list=[]
    for key1 in dict1.keys():
        for key2 in dict2.keys():
            if key1==key2:
               first_file=dict1[key1]
               second_file=dict2[key2]
               before=key1
               after=key2
               first_file_lines=open(first_file).readline()
               second_file_lines=open(second_file).readline()
               difference=difflib.HtmlDiff().make_file(first_file_lines, Second_file_lines,'Before'+before, 'After '+after)
               difference_report=open(key1+'.html','w')
               difference_report.write(difference)
               difference_report.close()
               diff_file_list.append(key1+'.html')
    return diff_file_list  
                 
 def display(message_list,h_size):
     star ='*'
     space =' '
     print star*(h_size+8)
     index=0
     for message in message_list:
          index=index+1
          if index==1:
              print star*2,space*(h_size+2),star*2
              rightspace=((h_size-len(message))/2)
              leftspace=(h_size-(rightspace+len(message)))
              print star*2, leftspace*, message, rightspace*space,star*2
          elif index==len(message_list):
              rightspace=((h_size-len(message))/2)
              leftspace=(h_size-rightspace+len(message)))
              print star*2, leftspace*space,message,rughtspace*space,star*2
              print star*2, space*(h_size+2,star*2
          else:
              rightspace=((h_size-len(message))/2)
              leftspace=(h_size-(rightspace+len(message)))
              print star*2, leftspace*space,message,rightspace*space,star*2
     print star*(h_size+8)
                 
                 
    
    
    
