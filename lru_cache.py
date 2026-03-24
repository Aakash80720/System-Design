
class LRUCache:
    def __init__(self, key, value, time_stamp):
        self.key = key
        self.value = value
        self.time_stamp = time_stamp

class LRUCacheOrderList:
    def __init__(self):
        self.value = None
        self.prev = None
        self.next = None
        

    def insert(self, node : LRUCache):
        node.next = self.value
        if self.value:
            self.value.prev = node
        self.value = node

    def remove(self, node : LRUCache):
        if node and node.prev:
            node.prev.next = node.next
        if node and node.next:
            node.next.prev = node.prev
        if self.value == node:
            self.value = node.next
        node.prev = None
        node.next = None

    def move_to_front(self, node: LRUCache):
        self.remove(node)
        self.insert(node)

    def display(self):
        current = self.value
        while current:
            print(f"Key: {current.key}, Value: {current.value}, Time Stamp: {current.time_stamp}")
            current = current.next


class LRUCacheSystem:
    def __init__(self, capacity):
        self.capacity  = capacity
        self.cache : dict[int, LRUCache] = {}
        self.order_list = LRUCacheOrderList()
        self.time = 0

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self.order_list.move_to_front(node)
            return node.value
        return -1
    
    def put(self, key, value):
        print(f"Putting key: {key}", self.cache)
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self.order_list.move_to_front(node)
        else:
            if len(self.cache) >= self.capacity :
                lru_node = self.order_list.value
                self.order_list.remove(lru_node)
                del self.cache[lru_node.key]
            new_node = LRUCache(key, value, self.time)
            self.cache[key] = new_node
            self.order_list.insert(new_node)
        self.time += 1

class LRUCacheInstructionParser:
    def __init__(self, instructions):
        self.instructions = instructions
        self.cache_system = None

    def execute(self):
        for instruction in self.instructions:
            if instruction[0] == "LRUCache":
                self.cache_system = LRUCacheSystem(instruction[1])
            elif instruction[0] == "put":
                self.cache_system.put(instruction[1], instruction[2])
            elif instruction[0] == "get":
                print(self.cache_system.get(instruction[1]))
            elif instruction[0] == "display":
                self.cache_system.order_list.display()


# Example usage:
instructions = [
    ["LRUCache", 2],
    ["display"],
    ["put", 1, 1],
    ["display"],
    ["put", 2, 2],
    ["display"],
    ["get", 1],
    ["display"],
    ["put", 3, 3],
    ["display"],
    ["get", 2],
    ["display"],
    ["put", 4, 4],
    ["display"],
    ["get", 3],
    ["get", 4],
    ["display"]
]   
parser = LRUCacheInstructionParser(instructions)
parser.execute()