#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 22:13:34 2019

@author: brian
"""

import math 

def prime_checker(n):
    #Checks if a number if prime by searching up to sqrt(n)
    assert (n > 0), "n must be positive!"
    if (n > 1):    
        a = 2 
        while (a <= (math.sqrt(n))):
            if n % a == 0:
                return False
            a += 1
    return True
            
def prime_generator(n):
    #Generates a list of prime numbers from 1 to n
    assert (n > 0), "n must be positive!"
    output = []
    for i in range(1, n + 1):
        if prime_checker(i):
            output.append(i)
    return output
