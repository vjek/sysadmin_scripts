#!/usr/bin/env python3
# rt_watchdog, reverse tunnel watchdog.
# Creates, monitors, and respawns ssh reverse tunnels.
# --
# ~/.ssh/config host1 entry:
#
#Host host1
#   ServerAliveCountMax 2
#   ServerAliveInterval 30
#   TCPKeepAlive yes
#   CheckHostIP no
#   User my_user_name
#   HostKeyAlias host1
#   HostName target.duckdns.org
#for proxychains:
#   DynamicForward 65222
#for sshing back on localhost
#   RemoteForward 2222 127.0.0.1:22
#   ForwardX11 no
#   Port 443
#   ExitOnForwardFailure yes
#
# --
# ~/.config/systemd/user/rt_watchdog.service contents: <- same regardless of UID
# [Unit]
# Description=rt_watchdog daemon
#
# [Service]
# Type=simple
# ExecStart=/usr/bin/env python3 /home/my_user_name/bin/rt_watchdog.py
# Restart=always
# RestartSec=10
#
# [Install]
# WantedBy=default.target
# --commands to daemonize script:
# loginctl enable-linger my_user_name <- username
# mkdir -p ~/.config/systemd/user/ <- not a typo, same regardless of username
# systemctl --user enable rt_watchdog.service
# systemctl --user start rt_watchdog.service
# systemctl --user status rt_watchdog.service
# --
# usage would be ssh -p 2222 my_user_name@127.0.0.1 on the destination.
# This would use the outbound connection to connect to the source SSH server.
# Any number of listeners/servers could be created in this fashion.
# If ~64k listeners isn't enough, multiple loopback addresses could be used as well,
# or just to conveniently map /etc/host names, and all use the same port number.
###
import subprocess,time,signal,syslog
from random import randint

def signal_handler(sig, frame):
    print('\nYou pressed Ctrl+C!')
    try:
        proc.kill()
    except:
        pass
    exit()

def setup_syslog():
    syslog.openlog(ident="rt_watchdog",logoption=syslog.LOG_PID, facility=syslog.LOG_USER)
    return

def decode_it(message): #handles utf-8 bytes and returns a string if so
    if type(message) == bytes:
        message=message.decode('utf-8')
    return(message)

def log_it(message):
    syslog.syslog(syslog.LOG_INFO,message)
    return

def check_for_others():
    proc_limit = 3 #when one is running, and another tries to start, it reports 3
    #first check if any other instances of this are running
    spawn='/usr/bin/pgrep -fc watchdog.py'
    proc = subprocess.Popen(spawn, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    stdout,stderr = proc.communicate()
    stdout=str(stdout.decode().strip())
    #if they are, exit
    if int(stdout) >= proc_limit: #this counts how many there are running.
        decode_it(stdout)
        stdout=("Exiting, instance threshold exceeded: {}".format(stdout))
        log_it(stdout)
        exit()
    return

signal.signal(signal.SIGINT, signal_handler)
setup_syslog()
check_for_others()
spawn1=["/usr/bin/ssh", "-N", "host1"]
while True:
    try:
        proc = subprocess.Popen(spawn1, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    except:
        log_it("Exception, child process has failed to spawn.")
        time.sleep(randint(10,20))
        continue
    else:
        log_it("Success, child process was spawned as PID:{}".format(proc.pid))
        stdout,stderr = proc.communicate()
        stdout=decode_it(stdout)
        stderr=decode_it(stderr)
        if len(stdout) != 0:
            log_it("stdout:{}".format(stdout).strip())
        if len(stderr) != 0:
            pass
#            log_it("stderr:{}".format(stderr).strip())
        time.sleep(randint(10,20))
