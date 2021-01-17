from DataStructs import Node

class Stack: #Changed for tower of Hanoi implementation
    def __init__(self, name):
        self.top_item = None
        self.size = 0
        self.limit = 1000
        self.name = name
    
    def get_size(self):
        return self.size
    
    def get_name(self):
        return self.name
    
    def print_items(self):
        pointer = self.top_item
        print_list = []
        while pointer:
            print_list.append(pointer.get_value())
            pointer = pointer.get_next_node()
        print_list.reverse()
        print("{0} Stack: {1}".format(self.get_name(), print_list))
    
    def push(self, value):
        if self.has_space():
            item = Node(value)
            item.set_next_node(self.top_item)
            self.top_item = item
            self.size +=1
            print("Adding {0} to the {1} stack!".format(value, self.name))
        else:
            print("No room for {}!".format(value))
    
    def pop(self):
        if not self.is_empty():
            item_to_remove = self.top_item
            self.top_item = item_to_remove.get_next_node()
            self.size -= 1
            return item_to_remove.get_value()
        print("All out of pizza.")
    
    def peek(self):
        if not self.is_empty():
            return self.top_item.get_value()
        
    def has_space(self):
        return self.limit > self.size
    
    def is_empty(self):
        return self.size == 0


def runTheGame():
    stacks = []
    left_stack, middle_stack, right_stack = Stack("Left"), Stack("Middle"), Stack("Right")
    stacks += [left_stack, middle_stack, right_stack]
    num_disks = int(input("\nHow many disks do you want to play with?\n"))
    while num_disks < 3:
        num_disks = int(input("\nEnter a number greater than ot equal to 3\n"))
    for i in range(num_disks, 0, -1):
        left_stack.push(i)
    num_optimal_moves = 2 ** num_disks - 1
    
    def get_input():
        choises = [stack.get_name()[0] for stack in stacks]
        while True:
            for i in range(len(stacks)):
                name = stacks[i].get_name()
                letter = choises[i]
                print("Enter {0} for {1}".format(letter, name))
            user_input = input()
            if user_input in choises:
                for i in range(len(stacks)):
                    if user_input == choises[i]:
                        return stacks[i]
    
    num_user_moves = 0
    
    while right_stack.get_size() != num_disks:
        print("\n\n\n...Current Stacks...")
        for stack in stacks:
            stack.print_items()
        while True:
            print("\nWhich stack do you want to move from?\n")
            from_stack = get_input()
            print("\nWhich stack do you want to move to?\n")
            to_stack = get_input()
            if from_stack.is_empty():
                print("\n\nInvalid move. Try again")
            elif to_stack.is_empty() or from_stack.peek() < to_stack.peek():
                disk = from_stack.pop()
                to_stack.push(disk)
                num_user_moves += 1
                break
            else:
                print("\n\n Invalid move. Try again")
    print("\n\nYou completed the game in {0} moves, and the optimal number of moves is {1}".format(num_user_moves, num_optimal_moves))

#Uncomment line below to run the game
#runTheGame()


#Finding best algorithm for n disks:
def find_optimal_moves(n, first_stack, second, third): #Put n disks from first to third using second
    if n == 0:
        return
    find_optimal_moves(n-1, first_stack, third, second)
    print(str(first_stack) + "->" + str(third) + "\n")
    find_optimal_moves(n-1, second, first_stack, third)
    return

#find_optimal_moves(3, 'L', 'M', 'R')
