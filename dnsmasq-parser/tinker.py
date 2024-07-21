#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2024-07-08 23:10:31
# @Author  : jockemedlinux (jockemedlinux@gmail.com)
# @Link    : @jockemedlinux
# @Version : $Id$

import re

pattern = r'(\S.*\:\d.) (\S+) (\S+) (\S+) (\S+) (\S+)'
 
with open("dnsmasq.log", "r") as logfile:
    data = logfile.readlines()
    for line in data:
        match = re.match(pattern, "".join(line))
        print(line)

    _date = match.group(1)
    _type = match.group(3)
    _domain = match.group(4)
    _ip = match.group(6)
    
    print(f'Date: {_date:<30}\nType: {_type:<23}\nIP Address: {_ip:<20}\nLocation: {_domain:<25}')