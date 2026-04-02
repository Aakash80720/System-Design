class Node:
    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None

class DoubleLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def insert_in_asc(self, val):
        new_node = Node(val)
        if not self.head:
            self.head = new_node
            self.tail = new_node
            return

        if val < self.head.val:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
            return

        if val > self.tail.val:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
            return

        current = self.head
        while current and current.val < val:
            current = current.next

        new_node.prev = current.prev
        new_node.next = current
        current.prev.next = new_node
        current.prev = new_node

class KthLargest:
    def __init__(self, k: int, nums: list[int]):
        self.k = k
        self.dll = DoubleLinkedList()
        self.length = 0
        for num in nums:
            self.dll.insert_in_asc(num)
            self.length += 1

    def add(self, val: int) -> int:
        self.dll.insert_in_asc(val)
        self.length += 1
        
        target_idx = self.length - self.k
        
        curr = self.dll.head
        for _ in range(target_idx):
            curr = curr.next
            
        return curr.val
    
# Example usage:
k = 3
nums = [4, 5, 8, 2]
kthLargest = KthLargest(k, nums)
print(kthLargest.add(3))  # returns 4
print(kthLargest.add(5))  # returns 5
print(kthLargest.add(10)) # returns 5
print(kthLargest.add(9))  # returns 8
print(kthLargest.add(4))  # returns 8

