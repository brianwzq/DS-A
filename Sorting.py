""" A collection of sorting algorithms over linked lists 
Quicksort, mergesort, insertionsort, bubblesort
Author: Brian
"""

################## Implementation of singly-linked list ###################

class Node:
    def __init__(self, value, next_node):
        self.next_node = None
        self.value = value
    #The inability to backtrack in a singly linked list is designed to cause strokes
    
class Llist:
    def __init__(self):
        self.first_node = self.last_node = None 
        self.count = 0
    
    def print_list(self):
        current_node = self.first_node
        output = []
        for i in range(self.count):
            output.append(current_node.value)
            current_node = current_node.next_node
        print(output)
    
    def push(self, node):
        if self.count == 0:
            self.first_node = self.last_node = node
        else:
            node.next_node = self.first_node
            self.first_node = node
        self.count += 1
        
    def pop(self):
        assert(self.count != 0), "The list is empty!"
        output = self.first_node
        if self.count == 1:
            self.first_node = self.last_node = None
        elif self.count > 1:
            self.first_node = output.next_node
        self.count -= 1
        output.next_node = None
        return output

    def lappend(self, l2):
        #Appends a given list to the end of the list. 
        if l2 and l2.count > 0:
            if self.count > 0:
                self.last_node.next_node = l2.first_node
                self.last_node = l2.last_node
            else:
                self.first_node = l2.first_node
                self.last_node = l2.last_node
            self.count += l2.count
    
    def nappend(self, node):
        #Appends a given node to the end of the list. 
        if self.count == 0:
            self.first_node = self.last_node = node
        else:
            self.last_node.next_node = node
            self.last_node = node
        self.count += 1
    
    def remove_node(self, index):
        #Removes the node at the given index and returns it. 
        assert(self.count > 0), "The list is empty!"
        assert(0 <= index < self.count), "The index is out of bounds!" 
        prior_node = self.first_node
        if index == 0:
            return self.pop()
        else:
            for i in range(index - 1):
                prior_node = prior_node.next_node
            returned_node = prior_node.next_node
            prior_node.next_node = returned_node.next_node
            if index == self.count - 1:
                self.last_node = prior_node
            self.count -= 1
            return prior_node
    
    def remove_segment(self, start, end):
        """Removes the segment between the given indexes as a list 
        We might be tempted to use remove and push on the start index for (end - start) times on start, 
        but remove requires that we traverse the list to the given index each time.
        Hence, this is highly inefficient. """
        assert(self.count > 0), "The list is empty!"
        assert(0 <= start < self.count), "The starting index is not within bounds."
        assert(0 <= end < self.count), "The ending index is not within bounds."
        assert(start <= end), "The end index cannot be higher than the start!"
        return_list = Llist()
        start_node = prior_node = self.first_node
        for i in range(start):
            start_node = start_node.next_node
            if i == start - 2: #This only runs if the start index is non-zero, so we have no wasted steps.
                prior_node = start_node
        end_node = start_node
        for i in range(end-start):
            end_node = end_node.next_node
        if start == 0 and end == self.count - 1:
            self.first_node = self.last_node = None
        elif start == 0:
            self.first_node = end_node.next_node
        elif end == self.count - 1:
            prior_node.next_node = None
            self.last_node = prior_node
        else:
            prior_node.next_node = end_node.next_node
        self.count -= (end - start + 1)
        return_list.first_node = start_node
        return_list.last_node = end_node
        return_list.count += (end - start + 1)
        return return_list

    def reverse(self):
        temp_list = Llist()
        while (self.first_node):
            temp_list.push(self.pop())
        self.lappend(temp_list)
    
    def check_sorted_traverse(self, node):
        if (node.next_node):
            return ((node.value <= node.next_node.value) and self.check_sorted_traverse(node.next_node))
        else:
            return True
        
    def check_sorted(self):
        return self.check_sorted_traverse(self.first_node) 

######## Sorting functions from here on out ###############
        
    """ Quicksort
    We choose the first element to be our pivot """

    def quick_sort(self):
        if (self.count > 1):
            mid = self.pop()
            start = Llist()
            end = Llist()
            for i in range(self.count):
                if self.first_node.value <= mid.value:
                    start.push(self.pop())
                else:
                    end.push(self.pop())
            start.quick_sort()
            self.lappend(start)
            self.nappend(mid)
            end.quick_sort()
            self.lappend(end)

    """ Mergesort 
    We need a helper function that merges two lists in order. """

    def merge(self, l):
        if l.count != 0:
            if self.count == 0:
                self.lappend(l)
            else:
                temp_list = Llist()
                """We push then reverse at the end because 
                it's faster than constantly using nappend for most implementations,
                though not this one because our linked list tracks the last node. """
                while (self.first_node or l.first_node):
                    if (self.first_node and l.first_node):
                        if self.first_node.value > l.first_node.value:
                            temp_list.push(l.pop())
                        elif self.first_node.value == l.first_node.value:
                            temp_list.push(l.pop())
                            temp_list.push(self.pop())
                        else:
                            temp_list.push(self.pop())
                    elif self.first_node:
                        temp_list.push(self.pop())
                    else:
                        temp_list.push(l.pop())
                temp_list.reverse()
                self.lappend(temp_list)
    
    def merge_sort(self):
        if self.count == 2:
            if self.first_node.value > self.last_node.value:
                self.reverse()
        elif self.count > 2:
            second = self.remove_segment(int(self.count/2), self.count - 1)
            self.merge_sort()
            second.merge_sort()
            self.merge(second)
            
    """ Insertionsort """  

    def search_and_insert(self, node, llist):
        if llist.count == 0 or (llist.first_node.value >= node.value):
            llist.push(node)
        elif llist.last_node.value < node.value:
            llist.nappend(node)
        else:
            prior_node = llist.first_node
            current_node = prior_node.next_node
            while current_node:
                if prior_node.value <= node.value <= current_node.value:
                    prior_node.next_node = node 
                    node.next_node = current_node
                    llist.count += 1
                    break
                current_node = current_node.next_node
                prior_node = prior_node.next_node
        
    def insertion_sort(self):
        if self.count > 1:
            new_list = Llist()
            for i in range(self.count):
                current_node = self.pop()
                self.search_and_insert(current_node, new_list)
            self.lappend(new_list)

    """Bubblesort """ 

    def check_and_swap_initial(self):
        #Swaps the two nodes at the head of the list if they are unsorted, and returns True if it does. 
        assert(self.count >= 2), "The list is too small!"
        if self.first_node.value > self.first_node.next_node.value:
            node = self.pop()
            node.next_node = self.first_node.next_node 
            self.first_node.next_node = node
            self.count += 1
            return True
        else:
            return False

    def check_and_swap_subsequent(self, first_node):
        #At node 1, swaps node 2 and 3 if they are unsorted, and returns True if it does. 
        second_node = first_node.next_node
        third_node = second_node.next_node
        if second_node.value > third_node.value:
            first_node.next_node = third_node
            second_node.next_node = third_node.next_node
            third_node.next_node = second_node
            return True
        else:
            return False
    
    """We define these two helper functions above rather than define a general
    check_and_swap function which operates on an index because that function
    would traverse the entire list each time it is called, which is highly 
    inefficient."""
    
    def bubble_sort(self):
        if (self.count > 1):
            flag = True
            if self.check_and_swap_initial():
                flag = False
            current_node = self.first_node
            while (current_node.next_node.next_node):
                if self.check_and_swap_subsequent(current_node):
                    flag = False
                current_node = current_node.next_node
            if not flag:
                self.bubble_sort()

######################  Testing #########################

import random
    
def test_sort():
    #Tests all the four sorting functions above. 
    print("Testing the quick_sort function...")
    test_list = Llist()
    for i in range(1000):
        new_node = Node(random.randint(0, 10000), None)
        test_list.push(new_node)
    if (not test_list.check_sorted()): #Just in case by some fluke we randomly generate an already sorted list. 
        test_list.quick_sort()
        if test_list.check_sorted():
            print("Testing complete. The quick_sort function worked!")
        else:
            print("Testing complete. The quick_sort function failed!")
    else:
        print("The initial list, by some miracle, was not sorted. Run it again!")
    print("Testing the merge_sort function...")
    test_list = Llist()
    for i in range(200):
        new_node = Node(random.randint(0, 10000), None)
        test_list.push(new_node)
    if (not test_list.check_sorted()): #Just in case by some fluke we randomly generate an already sorted list. 
        test_list.merge_sort()
        if test_list.check_sorted():
            print("Testing complete. The merge_sort function worked!")
        else:
            print("Testing complete. The merge_sort function failed!")
    else:
        print("The initial list, by some miracle, was not sorted. Run it again!")
    print("Testing the insertion_sort function...")
    test_list = Llist()
    for i in range(200):
        new_node = Node(random.randint(0, 10000), None)
        test_list.push(new_node)
    if (not test_list.check_sorted()): #Just in case by some fluke we randomly generate an already sorted list. 
        test_list.insertion_sort()
        if test_list.check_sorted():
            print("Testing complete. The insertion_sort function worked!")
        else:
            print("Testing complete. The insertion_sort function failed!")
    else:
        print("The initial list, by some miracle, was not sorted. Run it again!")
    print("Testing the bubble_sort function...")
    test_list = Llist()
    for i in range(200):
        new_node = Node(random.randint(0, 10000), None)
        test_list.push(new_node)
    if (not test_list.check_sorted()): #Just in case by some fluke we randomly generate an already sorted list. 
        test_list.bubble_sort()
        if test_list.check_sorted():
            print("Testing complete. The bubble_sort function worked!")
        else:
            print("Testing complete. The bubble_sort function failed!")
    else:
        print("The initial list, by some miracle, was not sorted. Run it again!")

if __name__ == '__main__':
    test_sort()

############################# End #################################