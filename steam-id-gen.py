#!/usr/bin/env python3
# 0000000100010000000000000000000100000000000000000000000000000010 76561197960265730
# creates "valid" public user steamID64's from random binary fields, where appropriate
# produces 4 by default, will produce as many as you specify as first integer argument
# based on: https://developer.valvesoftware.com/wiki/SteamID
# by vjek, 20200922
##
# The lowest bit represents Y.
# The next 31 bits represents the account number.
# The next 20 bits represents the instance of the account. It is usually set to 1 for user accounts.
# The next 4 bits represents the type of account.
# The next 8 bits represents the "Universe" the steam account belongs to.
# .. this means from right to left, 32 random bits, then
# 20 bits with a single 1, then
# 4 bits of type of account, 1 is single user
# 8 bits of universe, 1 is public.
# so we use: 00000001000100000000000000000001 instance, type, universe (R to L)
# checks: http://steamcommunity.com/profiles/76561198890353885 (random example)
# and https://steamidfinder.com/lookup/ (advanced tab for multi-line input)

import random,sys

#compute the 2's complement of int value
def twos_comp(val, bits):
    if (val & (1 << (bits - 1))) != 0: # if sign bit / most significant is set..
        val = val - (1 << bits)        # compute negative value
    return val                         # return positive value as is

#produce the 31+1 bits (Z+Y) according to the valve documentation
def get_zy():
    zy=''
    for a in range(32):         # generate account number and lowest bit
        bit=random.randint(0,1)
        zy=zy + str(bit)        # add each one onto the string
    return(zy)                  # return the random 32 0's and 1's

if __name__ == '__main__':
    count = 4
    if sys.argv[1:]:
        count = int(sys.argv[1]) #print out 4 unless otherwise specified

    for x in range(0,count):
        valve_binary = '00000001000100000000000000000001'+get_zy()   # add random to base
#        print(valve_binary) #optionally print it before conversion
        steam_id = twos_comp(int(valve_binary,2), len(valve_binary)) # create steamID64
        print(steam_id)
