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


# Our LinkedList class
class LinkedList:
  def __init__(self, value=None):
    self.head_node = Node(value)
  
  def get_head_node(self):
    return self.head_node
  
  
  def insert_beginning(self, new_value):
    new_node = Node(new_value, self.head_node)
    self.head_node = new_node

  def aux(self, node, acc):
    acc.append(str(node.get_value()))
    next_node = node.get_next_node()
    if (next_node is None):
      return acc
    else:
      return self.aux(next_node, acc)

  def stringify_list(self):
    head_node = self.get_head_node()
    acc = self.aux(head_node, [])
    #for i in acc:
      #print(i)
    s = '\n'.join(acc)
    return s


# Test
ll = LinkedList(5)
ll.insert_beginning(70)
ll.insert_beginning(5675)
ll.insert_beginning(90)
print(ll.stringify_list())
