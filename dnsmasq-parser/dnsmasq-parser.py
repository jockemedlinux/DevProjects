#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2024-07-07
# @Author  : jockemedlinux (jockemedlinux@gmail.com)
# @Link    : @jockemedlinux
# @Version : v0.1

import sys, re, platform, os 
class colors:
    MAGENTA = '\033[95m'            
    BLUE = '\033[94m'               
    CYAN = '\033[96m'               
    GREEN = '\033[92m'              
    ORANGE = '\033[93m'        
    YELLOW='\033[0;33m'
    RED = '\033[91m'                
    BLACK = '\033[0;30m'        
    PURPLE = '\033[0;35m'       
    WHITE = '\033[0;37m'        
    RESET = '\033[0m'

def banner():
    clearscreen()
    print(rf"""{colors.MAGENTA} 

    .___                                                                                          
  __| _/____   ______ _____ _____    ____________         ___________ _______  ______ ___________ 
 / __ |/    \ /  ___//     \\__  \  /  ___/ ____/  ______ \____ \__  \\_  __ \/  ___// __ \_  __ \
/ /_/ |   |  \\___ \|  Y Y  \/ __ \_\___ < <_|  | /_____/ |  |_> > __ \|  | \/\___ \\  ___/|  | \/
\____ |___|  /____  >__|_|  (____  /____  >__   |         |   __(____  /__|  /____  >\___  >__|   
     \/    \/     \/      \/     \/     \/   |__|         |__|       \/           \/     \/       

A dnsmasq-queries parser for easy overview.
---------------------------------------------------------------------------
Author:     @jockemedlinux 
Date:       2024-07-07
Version:    0.1
""")

def clearscreen():
    if "Linux" in platform.system():
        os.system("clear")
    elif "Windows" in platform.system():
        os.system("cls")
    elif "Mac" in platform.system():
        print("Looser")

#re_ip = r'(\b25[0-5]|\b2[0-4][0-9]|\b[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}'
rfilter = r'query.+|cached.+|forwarded.+|reply.+'

queries = []
forwarded = []
cached = []
reply = []
nxdomain = []


with open("dnsmasq.log", "r") as logfile:
	data = logfile.read()
	regex = re.findall(rfilter, data)
	
	#Counters
	count = 0
	count_q	= 0
	count_f	= 0
	count_c	= 0
	count_r	= 0
	count_nx = 0
	
	for line in regex:
		if 'query' in line:
			queries.append(line)
			count_q += 1
		elif 'forwarded' in line:
			forwarded.append(line)
			count_f += 1
		elif 'cached' in line:
			cached.append(line)
			count_c += 1
		elif 'reply' in line:
			reply.append(line)
			count_r += 1
		if 'NXDOMAIN' in line:
			nxdomain.append(line)
			count_nx += 1
		count += 1

clearscreen()
banner()

#STATISTICS
print("GENERAL STATISTICS: " + "\n" + "-" * 100)
print(f'{count_q:<11} Total queries from hosts')
print(f'{count_f:<11} Total forwarded responses')
print(f'{count_c:<11} Total cached responses')
print(f'{count_r:<11} Total replies.')
print(f'{count_nx:<11} Total failed with NXDOMAIN')
print(f'{count:<11} Total instances recorded.\n{colors.RESET}')

#Queries
print("Top 10 queries: " + "\n" + "-" * 100) 
print(f'{colors.GREEN}{"\n".join(queries[0:5])}{colors.RESET}' + "\n" )

#Forwards
print("Top 10 forwards: " + "\n" + "-" * 100) 
print(f'{colors.YELLOW}{"\n".join(forwarded[0:5])}{colors.RESET}' + "\n" )

#Cached
print("Top 10 cached: " + "\n" + "-" * 100)
print(f'{colors.BLUE}{"\n".join(cached[0:5])}{colors.RESET}' + "\n" )

#Replies
print("Top 10 replies: " + "\n" + "-" * 100) 
print(f'{colors.CYAN}{"\n".join(reply[0:5])}{colors.RESET}' + "\n" )

#NXDOMAINS
print("Top 10 nxdomains: " + "\n" + "-" * 100) 
print(f'{colors.RED}{"\n".join(nxdomain[0:5])}{colors.RESET}' + "\n" )