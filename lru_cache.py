class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self,capacity):
        self.capacity = capacity
        self.cache = {}
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add(node)
            return node.value
        return -1
    
    def put(self, key, value):
        if key in self.cache:
            self._remove(self.cache[key])
        node = Node(key=key, value=value)
        self._add(node)
        self.cache[key] = node
        if len(self.cache) > self.capacity:
            lru_node = self.tail.prev
            self._remove(lru_node)
            del self.cache[lru_node.key]

    def display(self):
        current = self.head.next
        while current != self.tail:
            print(f"Key {current.key}: Value {current.value}", end=" -> ")
            current = current.next
        print("NULL")
    
    class LRUInstructionFactory:
        @staticmethod
        def excute_instruction(cache, instruction):
            if instruction[0] == "get":
                return cache.get(instruction[1])
            elif instruction[0] == "display":
                cache.display()
            elif instruction[0] == "LRUCache":
                return LRUCache(instruction[1])
            elif instruction[0] == "put":
                cache.put(instruction[1], instruction[2])
# Example usage:
if __name__ == "__main__":
    instructions = [
        ["LRUCache", 2],
        ["put", 1, 1],
        ['display'],
        ["put", 2, 2],
        ['display'],
        ["get", 1],
        ['display'],
        ["put", 3, 3],
        ['display'],
        ["get", 2],
        ['display'],
        ["put", 4, 4],
        ['display'],
        ["get", 3],
        ["get", 4],
        ["display"]
    ]

    cache = None
    for instruction in instructions:
        result = LRUCache.LRUInstructionFactory.excute_instruction(cache, instruction)
        if instruction[0] == "LRUCache":
            cache = result

    