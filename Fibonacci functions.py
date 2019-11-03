#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: brian

Fibonacci functions of varying complexities

By definition, we take the first two numbers (indexes 1 and 2) of our
Fibonacci sequence to be 1 and 2.

"""
import unittest 

###############################################################################

#Fib function using simple recursion

def fib_simple(n):
    #Simple recursion
    #Exponential (base 2) time and space complexity
    if (n == 1 or n == 2):
        return 1
    else:
        return fib_simple(n - 1) + fib_simple(n - 2)
    
###############################################################################  
        
#Fib function using an accumulator
    
def fib_better(n):
    #Using an accumulator
    #Linear time and constant space 
    a = b = 1
    if (n == 1 or n == 2):
        return b
    else:
        while (n > 2):
            b = a + b
            a = b - a
            n += -1 
    return b

###############################################################################
    
#Helper functions for matrix multiplication 
    
def matrix_mult(m, n):
    #Takes two 2 x 2 matrices and returns their product
    output = [[0, 0], [0, 0]]
    for i in range(2):
        for j in range(2):
            output[i][j] = m[i][0]*n[0][j]+m[i][1]*n[1][j]
    return output

def matrix_exp_linear(m, n):
    #A matrix exponentiation function for 2 by 2 matrices 
    #Linear time, constant space
    base = m
    while (n > 1):
        m = matrix_mult(m, base)
        n -= 1
    return m

def matrix_exp_exp(m, n):
    #A matrix exponentiation function for 2 by 2 matrices 
    #Logarithmic, constant space
    resid_prod = [[1, 0], [0, 1]]
    while (n > 1):
        if (n % 2) == 0:
            m = matrix_mult(m, m)
            n /= 2
        else:
            resid_prod = matrix_mult(resid_prod, m)
            n -= 1
    return matrix_mult(m, resid_prod )

###############################################################################

#Fib functions using matrix multiplication 

def fib_matrix_linear(n):
    #A fib function using linear matrix exponentiation of the matrix [[0, 1], [1, 1]]
    #Linear time, constant space
    base = [[0, 1], [1, 1]]
    return matrix_exp_linear(base, n)[1][0]

def fib_matrix_log(n):
    #A fib function using logarithmic matrix exponentiation of the matrix [[0, 1], [1, 1]]
    #Log time, constant space
    base = [[0, 1], [1, 1]]
    return matrix_exp_exp(base, n)[1][0]

###############################################################################
    
#A logarithmic fib function using the identity 
#fib (p + q + 1) = fib (p + 1) * fib (q + 1) + fib p * fib q
        
def fib_best(n):
    if (n == 0):
        return 0
    elif (n == 1):
        return 1
    else: 
        if (n % 2 == 0):
            big = fib_best(n/2)
            small = fib_best(n/2 - 1)
            return ((big + small) * big + small * big)
        else:
            big = fib_best((n + 1)/2)
            small = fib_best((n - 1)/2)
            return (big * big + small * small)

###############################################################################     
        
class TestMean(unittest.TestCase): 

    def setUp(self): 
        pass

    def test_fib_accum(self):
        self.assertEqual(fib_better(10), 55) 
        self.assertEqual(fib_better(20), 6765) 
        self.assertEqual(fib_better(30), 832040)
        self.assertEqual(fib_better(100), 354224848179261915075)
        
    def test_fib_matrix_linear(self):
        self.assertEqual(fib_matrix_linear(10), 55) 
        self.assertEqual(fib_matrix_linear(20), 6765) 
        self.assertEqual(fib_matrix_linear(30), 832040)
        self.assertEqual(fib_matrix_linear(100), 354224848179261915075)    
    
    def test_fib_matrix_log(self):
        self.assertEqual(fib_matrix_log(10), 55) 
        self.assertEqual(fib_matrix_log(20), 6765) 
        self.assertEqual(fib_matrix_log(30), 832040)
        self.assertEqual(fib_matrix_log(100), 354224848179261915075)
        
    def test_fib_best(self):
        self.assertEqual(fib_best(10), 55) 
        self.assertEqual(fib_best(20), 6765) 
        self.assertEqual(fib_best(30), 832040)
        self.assertEqual(fib_best(100), 354224848179261915075)
        
if __name__ == '__main__': 
    unittest.main()

#All unit tests passed




