#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2025-07-03
# @Author  : jockemedlinux (jockemedlinux@gmail.com)
# @Link    : @jockemedlinux
# @Version : $##v0.11##

import re
import sys
import platform
import os
import argparse
from collections import Counter

# DEFINE TERMINAL COLORS FOR APPEARANCE
class colors:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'

def clearscreen():
    if "Linux" in platform.system():
        os.system("clear")
    elif "Windows" in platform.system():
        os.system("cls")
    elif "Mac" in platform.system():
        print("Looser")

def banner():
    clearscreen()
    print(rf"""{colors.GREEN}
 _  _  ____  _  _      ____   __   ____  ____  ____  ____ 
/ )( \(  __)/ )( \ ___(  _ \ / _\ (  _ \/ ___)(  __)(  _ \
) \/ ( ) _) \ /\ /(___)) __//    \ )   /\___ \ ) _)  )   /
\____/(__)  (_/\_)    (__)  \_/\_/(__\_)(____/(____)(__\_)
{colors.RESET}
A Uncomplicated FireWall (UFW) Log-parser.
---------------------------------------------------------------------------
Author:     @jockemedlinux 
Date:       2024-06-27
Version:    0.1
""")

def entries_mode(entries, color, max_lines=None):
    try:
        print(color)
        header = f"{'Source IP:':<20}{'Destination IP:':<20}{'Protocol:':<20}{'Source Port:':<20}{'Destination Port:':<20}{'Count:':<20}"
        print(header)
        print('-' * len(header))

        ip_counter = Counter()
        entry_dict = []

        for entry in entries:
            src_match = re.search(r'SRC=([\d.]+)', entry)
            dst_match = re.search(r'DST=([\d.]+)', entry)
            proto_match = re.search(r'PROTO=(\S+)', entry)
            spt_match = re.search(r'SPT=([\d.]+)', entry)
            dpt_match = re.search(r'DPT=([\d.]+)', entry)

            if src_match and dst_match and proto_match and spt_match and dpt_match:
                src = src_match.group(1)
                dst = dst_match.group(1)
                proto = proto_match.group(1)
                spt = spt_match.group(1)
                dpt = dpt_match.group(1)

                ip_counter[src] += 1
                ip_counter[dst] += 1

                entry_dict.append({
                    "src": src,
                    "dst": dst,
                    "proto": proto,
                    "spt": spt,
                    "dpt": dpt,
                    "count": ip_counter[src]
                })

        
        sorted_entries = sorted(entry_dict, key=lambda x: x["count"], reverse=True)

        # Limit to max_lines if specified
        if max_lines:
            sorted_entries = sorted_entries[:max_lines]

        for entry in sorted_entries:
            print(f"{entry['src']:<20}{entry['dst']:<20}{entry['proto']:<20}{entry['spt']:<20}{entry['dpt']:<20}{entry['count']:<20}")

        print(colors.RESET)

    except KeyboardInterrupt:
        print(colors.RED + "\nProgram stopped by user. Exiting..." + colors.RESET)
        sys.exit(1)

def ip_mode(data, max_lines=None):
    ip_counter = Counter()
    for entry in data:
        src_match = re.search(r'SRC=([\d.]+)', entry)
        dst_match = re.search(r'DST=([\d.]+)', entry)
        if src_match:
            ip_counter[src_match.group(1)] += 1
        if dst_match:
            ip_counter[dst_match.group(1)] += 1

    sorted_ips = sorted(ip_counter.items(), key=lambda x: x[1], reverse=True)    
    print(colors.BLUE + "Top IP Addresses by occurrence:\n" + colors.RESET)
    print(f"{colors.BLUE}{'IP Address':<20}{'Count':<10}{colors.RESET}")
    print('-' * 75)
    
    if max_lines:
        sorted_ips = sorted_ips[:max_lines]  # Truncate IPs if max_lines is specified
    
    for ip, count in sorted_ips:
        if count > 500:
            color = colors.RED
        elif count > 100:
            color = colors.YELLOW
        else:
            color = colors.GREEN
        print(f"{color}{ip:<20}{count:<10}{colors.RESET}")

def main():
    banner()
    parser = argparse.ArgumentParser('ufw-parser.py')
    parser.add_argument("-f", "--file", help="Specify location of your ufw.log file", metavar="", default="/var/log/ufw.log", required=True)
    parser.add_argument("-e ", "--entries", action="store_true", help="'Entries mode'")
    parser.add_argument("-i ", "--ip", action="store_true", help="'IP mode'")
    parser.add_argument("-n", "--lines", type=int, help="Specify how many lines you want to output.", metavar="")
    args = parser.parse_args()

    data = []
    with open(args.file, "r") as file:
        for line in file:
            matches = re.findall(r'\[UFW[^\]]*\]|SRC=[\d.]+|DST=[\d.]+|PROTO=\S+|SPT=[\d.]+|DPT=[\d.]+', line)
            if matches:
                joined = ' '.join(matches)
                data.append(joined)

    ALLOWED = [x for x in data if "[UFW ALLOW]" in x]
    BLOCKED = [x for x in data if "[UFW BLOCK]" in x]
    AUDITED = [x for x in data if "[UFW AUDIT]" in x]

    try:
        if args.entries:
            print(f'{colors.GREEN}[UFW ALLOWED]{colors.RESET}')
            entries_mode(ALLOWED, colors.GREEN, args.lines if args.lines else None)
            print(f'{colors.YELLOW}[UFW AUDITED]{colors.RESET}')
            entries_mode(AUDITED, colors.YELLOW, args.lines if args.lines else None)
            print(f'{colors.RED}[UFW BLOCKED]{colors.RESET}')
            entries_mode(BLOCKED, colors.RED, args.lines if args.lines else None)
        elif args.ip:
            ip_mode(data, args.lines if args.lines else None)
        else:
            parser.print_help()
    except KeyboardInterrupt:
        print(colors.RED + "\nProgram stopped. Exiting..." + colors.RESET)
        sys.exit(1)

if __name__ == "__main__":
    main()