"""

Author: Brian
Defining singly-linked lists of integers and a collection of methods over them. 
This implementation of a llist points to the first and last node of the llist.
A counter of the number of nodes in the llist is not stored.  

"""

class Node:
    def __init__(self, value, next_node):
        self.value = value
        self.next_node = next_node 

class LinkedList:
    def __init__(self):
        self.first_node = None #When the LL is first initialized, it is an empty list. 
        self.last_node = None
    
    #Let us define a collection of methods
    
    def print_list(self): #Printing all the elements of the list 
        output = []
        current_node = self.first_node
        while (current_node != None):
            output.append(current_node.value)
            current_node = current_node.next_node
        print (output)
        
    def cons(self, ll):
        #Appending the input list to the head of the list 
        if (ll.first_node != None):
            ll.last_node.next_node = self.first_node
            self.first_node = ll.first_node
        
    def append(self, ll):
        #Appending the input list to the tail of the list 
        if (self.first_node != None):
            self.last_node.next_node = ll.first_node 
            self.last_node = ll.last_node
        else:
            self.first_node = ll.first_node
            self.last_node = ll.last_node
            
    def reverse(self):
        pass
    
    def insert(self, node, index):
        pass 
    
    def pop(self):
        pass
    
    def remove(self, index):
        pass 

        
        
        
        
        
        
        
        
        
        