# Linear data structures implementation in Python

#Helper functions:
def tl(arr):
    return arr[1:]

def hd(arr):
    return arr[0]

def curry(f):
    curried = lambda x: lambda y: f(x, y)
    return curried


class Dops: #Class contain data operations
    def getNodesVals(self, node, acc):
        acc.append(str(node.get_value()))
        next_node = node.get_next_node()
        if (next_node == None):
            return acc
        else:
            return self.getNodesVals(next_node, acc)
        
    def swap_nodes(self, input_list, val1, val2):
        print(f'Swapping {val1} with {val2}')
        
        node1_prev = None
        node2_prev = None
        node1 = input_list.head_node
        node2 = input_list.head_node
        
        if val1 == val2:
            print("Elements are the same - no swap needed")
            return
        
        while node1 is not None:
            if node1.get_value() == val1:
                break
            node1_prev = node1
            node1 = node1.get_next_node()
            
        while node2 is not None:
            if node2.get_value() == val2:
                break
            node2_prev = node2
            node2 = node2.get_next_node()
      
        if (node1 is None or node2 is None):
            print("Swap not possible - one or more element is not in the list")
            return
        
        if node1_prev is None:
            self.head_node = node2
        else:
            node1_prev.set_next_node(node2)
            
            if node2_prev is None:
                input_list.head_node = node1
            else:
                node2_prev.set_next_node(node1)
                
            temp = node1.get_next_node()
            node1.set_next_node(node2.get_next_node())
            node2.set_next_node(temp)
            
    def linear_search(search_list, target_value):
        matches = []
        def f(lst, i):
            if i == len(search_list):
                return
            elif hd(lst) == target_value:
                matches.append(i)
                f(tl(lst), i+1)
            else:
                f(tl(lst), i+1)
        f(search_list, 0)
        if matches:
            return matches
        else:
            raise ValueError("{0} not in list".format(target_value))
        
    def binary_search(self, sorted_list, left_pointer, right_pointer, target):
        if left_pointer >= right_pointer: # indicate we've reached an empty "sub-list"
            return "value not found"
        mid_idx = (left_pointer + right_pointer) // 2
        mid_val = sorted_list[mid_idx]
        if mid_val == target:
            return mid_idx
        elif mid_val > target: # we reduce the sub-list by passing in a new right_pointer
            return self.binary_search(self, sorted_list, left_pointer, mid_idx, target)
        else: # we reduce the sub-list by passing in a new left_pointer
            return self.binary_search(self, sorted_list, mid_idx + 1, right_pointer, target)
        
    def binary_search_iterative(sorted_list, target):
        left_pointer = 0
        right_pointer = len(sorted_list)
        while left_pointer < right_pointer:
            mid_idx = (left_pointer+right_pointer)//2
            mid_val = sorted_list[mid_idx]
            if mid_val == target:
                return mid_idx
            if target < mid_val:
                right_pointer = mid_idx
            if target > mid_val:
                left_pointer = mid_idx + 1
        return "Value not in list"
    
    def sparse_search(data, search_val):
        print("Data: " + str(data))
        print("Search Value: " + str(search_val))
        first, last = 0, len(data) - 1
        while first <= last:
            mid = (first+last) // 2
            if not data[mid]:
                left, right = mid - 1, mid + 1
                while True:
                    if left < first and right > last:
                        print('{0} is not in the dataset'.format(search_val))
                        return
                    elif right <= last and data[right]:
                        mid = right
                        break
                    elif left >= first and data[left]:
                        mid = left
                        break
                    right +=1
                    left -= 1
            if data[mid] == search_val:
                print('{0} found at position {1}'.format(search_val, mid))
                return
            elif search_val < data[mid]:
                last = mid - 1
            elif search_val > data[mid]:
                first = mid + 1
        print('%s is not in the dataset' % search_val)

#Testing binary_search
#values = [77, 80, 102, 123, 288, 300, 540]
#start_of_values = 0
#end_of_values = len(values)
#result = aux.binary_search(aux, values, start_of_values, end_of_values, 288)
#print("element {0} is located at index {1}".format(288, result))

#Testing sparse_search
#Dops.sparse_search(["Alex", "", "", "", "", "Devan", "", "", "Elise", "", "", "", "Gary", "", "", "Mimi", "", "", "Parth", "", "", "", "Zachary"], "Parh")



# Classes of data structures:
class Node:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next_node = next_node
    
    def get_value(self):
        return self.value
  
    def get_next_node(self):
        return self.next_node
  
    def set_next_node(self, next_node):
        self.next_node = next_node


class LinkedList(Dops):
    def __init__(self, value=None):
        self.head_node = Node(value)
  
    def get_head_node(self):
        return self.head_node
  
    def insert_beginning(self, new_value):
        new_node = Node(new_value, self.head_node)
        self.head_node = new_node
    
    def stringify_list(self):
        head_node = self.get_head_node()
        acc = super().getNodesVals(head_node, [])
        s = '\n'.join(acc)
        return s


# Test
#ll = LinkedList(5)
#ll.insert_beginning(70)
#ll.insert_beginning(5675)
#ll.insert_beginning(90)
#print(ll.stringify_list())

#ll = LinkedList()
#for i in range(10):
#  ll.insert_beginning(i)

#print(ll.stringify_list())
#aux.swap_nodes(aux, ll, 3, 6)
#print(ll.stringify_list())

#---------------------
# #Doubly linked lists
#---------------------

#Apdated node class:
class Node:
    def __init__(self, value, next_node=None, prev_node=None):
        self.value = value
        self.next_node = next_node
        self.prev_node = prev_node
    
    def set_next_node(self, next_node):
        self.next_node = next_node
    
    def get_next_node(self):
        return self.next_node
    
    def set_prev_node(self, prev_node):
        self.prev_node = prev_node
    
    def get_prev_node(self):
        return self.prev_node
    
    def get_value(self):
        return self.value


#Doubly linked lists
class DoublyLinkedList:
    def __init__(self):
        self.head_node = None
        self.tail_node = None
        
    def add_to_head(self, new_value):
        new_head = Node(new_value)
        current_head = self.head_node
        if current_head != None:
            current_head.set_prev_node(new_head)
            new_head.set_next_node(current_head)
        self.head_node = new_head
        if self.tail_node == None:
            self.tail_node = new_head
            
    def add_to_tail(self, new_value):
        new_tail = Node(new_value)
        current_tail = self.tail_node
        if current_tail != None:
            current_tail.set_next_node(new_tail)
            new_tail.set_prev_node(current_tail)
        self.tail_node = new_tail
        if self.head_node == None:
            self.head_node = new_tail
            
    def remove_head(self):
        removed_head = self.head_node
        if removed_head == None:
            return None
        self.head_node = removed_head.get_next_node()
        if self.head_node != None:
            self.head_node.set_prev_node(None)
        if removed_head == self.tail_node:
            self.remove_tail()
        return removed_head.get_value()
    
    def remove_tail(self):
        removed_tail = self.tail_node
        if removed_tail == None:
            return None
        self.tail_node = removed_tail.get_prev_node()
        if self.tail_node != None:
            self.tail_node.set_next_node(None)
        if removed_tail == self.head_node:
            self.remove_head()
        return removed_tail.get_value()
    
    def remove_by_value(self, value_to_remove):
        node_to_remove = None
        current_node = self.head_node
        while current_node != None:
            if current_node.get_value() == value_to_remove:
                node_to_remove = current_node
                break
            current_node = current_node.get_next_node()
            if node_to_remove == None:
                return None
            if node_to_remove == self.head_node:
                self.remove_head()
            elif node_to_remove == self.tail_node:
                self.remove_tail()
            else:
                next_node = node_to_remove.get_next_node()
                prev_node = node_to_remove.get_prev_node()
                next_node.set_prev_node(prev_node)
                prev_node.set_next_node(next_node)
            return node_to_remove
        
    def stringify_list(self):
        string_list = ""
        current_node = self.head_node
        while current_node:
            if current_node.get_value() != None:
                string_list += str(current_node.get_value()) + "\n"
            else:
                current_node = current_node.get_next_node()
        return string_list

#tour_locations = [ "New York City", "Los Angeles", "Bangkok", "Istanbul", "London", "New York City", "Toronto"]
#target_city = "New York City"
#tour_stops = aux.linear_search(tour_locations, target_city)
#print(tour_stops)

# test cases
#print(aux.binary_search_iterative([5,6,7,8,9], 9))
#print(aux.binary_search_iterative([5,6,7,8,9], 10))
#print(aux.binary_search_iterative([5,6,7,8,9], 8))


#---------------------
#Queues
#---------------------


class Queue:
    def __init__(self, max_size=None):
        self.head = None
        self.tail = None
        self.max_size = max_size
        self.size = 0
    
    def enqueue(self, value):
        if self.has_space():
            item_to_add = Node(value)
            print("Adding " + str(item_to_add.get_value()) + " to the queue!")
            if self.is_empty():
                self.head, self.tail = item_to_add, item_to_add
            else:
                self.tail.set_next_node(item_to_add)
                self.tail = item_to_add
            self.size += 1
        else:
            print("Sorry, no more room!")
    
    def dequeue(self):
        if not self.is_empty():
            item_to_remove = self.head
            print("Removing " + str(item_to_remove.get_value()) + " from the queue!")
            if self.size == 1:
                self.head, self.tail = None, None
            else:
                self.head = self.head.get_next_node()
            self.size -= 1
            return item_to_remove.get_value()
        else:
            print("This queue is totally empty!")
        
    def peek(self):
        if not self.is_empty():
            return self.head.get_value()
        else:
            print ("Nothing to see here!")
            
    def get_size(self):
        return self.size
    
    def has_space(self):
        return (not self.max_size) or (self.max_size > self.get_size())
    
    def is_empty(self):
        return self.size == 0


#Uncomment to test
print("Creating a deli line with up to 10 orders...\n------------")
deli_line = Queue(10)
print("Adding orders to our deli line...\n------------")
#deli_line.enqueue("egg and cheese on a roll")
#deli_line.enqueue("bacon, egg, and cheese on a roll")
#deli_line.enqueue("toasted sesame bagel with butter and jelly")
#deli_line.enqueue("toasted roll with butter")
#deli_line.enqueue("bacon, egg, and cheese on a plain bagel")
#deli_line.enqueue("two fried eggs with home fries and ketchup")
#deli_line.enqueue("egg and cheese on a roll with jalapeos")
#deli_line.enqueue("plain bagel with plain cream cheese")
#deli_line.enqueue("blueberry muffin toasted with butter")
#deli_line.enqueue("bacon, egg, and cheese on a roll")

#deli_line.enqueue("western omelet with home fries")

#print("------------\nOur first order will be " + deli_line.peek())
#print("------------\nNow serving...\n------------")
#for i in range(11):
#    deli_line.dequeue()


#---------------------
#Stacks
#---------------------


class Stack:
    def __init__(self, limit=1000):
        self.top_item = None
        self.size = 0
        self.limit = limit
    
    def push(self, value):
        if self.has_space():
            item = Node(value)
            item.set_next_node(self.top_item)
            self.top_item = item
            self.size +=1
            print("Adding {} to the pizza stack!".format(value))
        else:
            print("No room for {}!".format(value))
    
    def pop(self):
        if not self.is_empty():
            item_to_remove = self.top_item
            self.top_item = item_to_remove.get_next_node()
            self.size -= 1
            print("Delivering " + item_to_remove.get_value())
            return item_to_remove.get_value()
        print("All out of pizza.")
    
    def peek(self):
        if not self.is_empty():
            return self.top_item.get_value()
        
    def has_space(self):
        return self.limit > self.size
    
    def is_empty(self):
        return self.size == 0

#Testing Stacks
#pizza_stack = Stack(6)
#for i in range(6):
#    pizza_stack.push("pizza {0}".format('#' + str(i)))

#pizza_stack.push("pizza #7")

#print("The first pizza to deliver is " + pizza_stack.peek())
#for i in range(7):
#    pizza_stack.pop()
