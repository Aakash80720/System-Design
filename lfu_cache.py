from collections import defaultdict

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.freq = 1
        self.prev = None
        self.next = None

class DoubleLinkedList:
    def __init__(self):
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def add_node(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
        self.size += 1

    def remove_node(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1

    def remove_tail(self):
        if self.size == 0: return None
        node = self.tail.prev
        self.remove_node(node)
        return node

class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {} # key -> Node
        self.freq_list_map = defaultdict(DoubleLinkedList)
        self.min_freq = 0

    def _update(self, node):
        """Helper to move a node to its next frequency list."""
        freq = node.freq
        self.freq_list_map[freq].remove_node(node)
        
        # If the list for min_freq is now empty, increment min_freq
        if freq == self.min_freq and self.freq_list_map[freq].size == 0:
            self.min_freq += 1
            
        node.freq += 1
        self.freq_list_map[node.freq].add_node(node)

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._update(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0: return

        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._update(node)
        else:
            if len(self.cache) >= self.capacity:
                # EVICT: Go to the list of the lowest frequency and pop the tail (LRU)
                lfu_node = self.freq_list_map[self.min_freq].remove_tail()
                if lfu_node:
                    del self.cache[lfu_node.key]
            
            # INSERT: New nodes always start at frequency 1
            new_node = Node(key, value)
            self.cache[key] = new_node
            self.min_freq = 1
            self.freq_list_map[1].add_node(new_node)

    def display(self):
        for freq, dll in self.freq_list_map.items():
            current = dll.head.next
            while current != dll.tail:
                print(f"Key {current.key}: Value {current.value}, Frequency {current.freq}", end=" -> ")
                current = current.next
        print("NULL")

class LFUInstructionFactory:
    @staticmethod
    def excute_instruction(cache, instruction):
        if instruction[0] == "get":
            return cache.get(instruction[1])
        elif instruction[0] == "display":
            return cache.display()
        elif instruction[0] == "put":
            cache.put(instruction[1], instruction[2])

        elif instruction[0] == "LFUCache":
            return LFUCache(instruction[1])
        
if __name__ == "__main__":
    """["LFUCache","put","put","get","get","put","get","get","get"]
[[2],[2,1],[3,2],[3],[2],[4,3],[2],[3],[4]]"""
    instructions = [
        ["LFUCache", 2],
        ["put", 2, 1],
        ["put", 3, 2],
        ["get", 3],
        ["get", 2],
        ["put", 4, 3],
        ["get", 2],
        ["get", 3],
        ["get", 4]
    ]
    """Expected Output:
[null,null,null,2,1,null,1,-1,3]"""
    cache = None
    for instruction in instructions:
        if instruction[0] == "LFUCache":
            cache = LFUInstructionFactory.excute_instruction(cache, instruction)
        else:
            result = LFUInstructionFactory.excute_instruction(cache, instruction)
            if result is not None:
                print(result)