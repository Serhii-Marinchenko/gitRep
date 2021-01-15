# Linear data structures implementation in Python

#Define helper superclass
class aux:
    def tl(arr):
        return arr[1:]
    
    def hd(arr):
        return arr[0]
    
    def curry(f):
        curried = lambda x: lambda y: f(x, y)
        return curried
    
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
            
    def linear_search(self, search_list, target_value):
        def f(lst, i):
            if self.hd(lst) == target_value:
                return i
            else:
                return f(self.tl(lst), i+1)
        try:
            ans = f(search_list, 0)
        except:
            ans = "{0} not in list".format(target_value)
        return ans


# Nodes 
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


class LinkedList(aux):
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
ll = LinkedList(5)
ll.insert_beginning(70)
ll.insert_beginning(5675)
ll.insert_beginning(90)
print(ll.stringify_list())

ll = LinkedList()
for i in range(10):
  ll.insert_beginning(i)

print(ll.stringify_list())
aux.swap_nodes(aux, ll, 3, 6)
print(ll.stringify_list())
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
    
