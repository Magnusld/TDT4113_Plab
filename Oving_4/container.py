"""This file contains the different container datastructures"""


class Container:
    """This is a superclass for the container datastructures"""
    items = None

    def __init__(self):
        self.items = []

    def size(self):
        """Returns the current amount of items in the container"""
        return len(self.items)

    def is_empty(self):
        """Returns a boolean value, that is true if the container is empty"""
        return len(self.items) == 0

    def push(self, item):
        """Adds a new item to end of top/end of the container"""
        self.items.append(item)

    def pop(self):
        """Remove the apropriate item from the container"""

    def peek(self):
        """Return the next item that would be poped, without removing it"""


class Stack(Container):
    """Implements the container superclass as a Stack"""
    def __init__(self):
        super().__init__()

    def pop(self):
        if not self.is_empty():
            return self.items.pop(-1)
        return None

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None


class Queue(Container):
    """Implements the container superclass as a Queue"""
    def __init__(self):
        super().__init__()

    def pop(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None

    def peek(self):
        if not self.is_empty():
            return self.items[0]
        return None

class ContainerTest:
    """A test class to see if the containers are implemented correctly"""

    def __main__(self):
        queue = Stack() #Just change "Stack" to "Queue" to test the other datastructure
        queue.push("1")
        queue.push("2")
        queue.push("3")
        queue.push("4")
        while not queue.is_empty():
            print(queue.peek())
            queue.pop()

if __name__ == '__main__':
    ContainerTest().__main__()
