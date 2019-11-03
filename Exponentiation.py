#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 15:38:58 2019

@author: brian
"""

def expo_linear(m, n):
    #An exponentiation function which does the job in linear time and constant space. 
    base = m
    while (n > 1):
        m = m * base
        n -= 1
    return m

def expo_log(m, n):
    #An exponentiation function which does the job in log time and constant space. 
    product = 1 
    while (n > 1):
        if (n % 2 == 0):
            m = m * m
            n /= 2
        else: 
            product *= m 
            m = m * m
            n -= 1 
            n /= 2
    else:
        return (product * m)