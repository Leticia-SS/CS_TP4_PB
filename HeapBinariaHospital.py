class BinaryHeap:
    def __init__(self):
        self.heap = []

    def is_empty(self):
        return len(self.heap) == 0

    def _parent(self, index):
        return (index - 1) // 2

    def _left_child(self, index):
        return 2 * index + 1

    def _right_child(self, index):
        return 2 * index + 2

    def _heapify_up(self, index):
        while index > 0:
            parent_index = self._parent(index)
            if self.heap[index]['priority'] < self.heap[parent_index]['priority']:
                self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
                index = parent_index
            else:
                break

    def _heapify_down(self, index):
        size = len(self.heap)
        while True:
            left_child = self._left_child(index)
            right_child = self._right_child(index)
            smallest = index

            if left_child < size and self.heap[left_child]['priority'] < self.heap[smallest]['priority']:
                smallest = left_child

            if right_child < size and self.heap[right_child]['priority'] < self.heap[smallest]['priority']:
                smallest = right_child

            if smallest != index:
                self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
                index = smallest
            else:
                break

    def insert(self, item):
        self.heap.append(item)
        self._heapify_up(len(self.heap) - 1)

    def find_min(self):
        if self.is_empty():
            return None
        return self.heap[0]

    def extract_min(self):
        if self.is_empty():
            return None

        min_item = self.heap[0]
        last_item = self.heap.pop()

        if self.heap:
            self.heap[0] = last_item
            self._heapify_down(0)

        return min_item

    def build_heap(self, items_list):
        self.heap = items_list[:]

        for i in range(len(self.heap) // 2 - 1, -1, -1):
            self._heapify_down(i)


# Teste
if __name__ == "__main__":
    patients = [
        {'name': 'João', 'priority': 3},
        {'name': 'Maria', 'priority': 1},
        {'name': 'Pedro', 'priority': 4},
        {'name': 'Ana', 'priority': 2},
        {'name': 'Mariana', 'priority': 5},
        {'name': 'Rafael', 'priority': 2},
        {'name': 'Carolina', 'priority': 3}
    ]

    heap = BinaryHeap()
    heap.build_heap(patients)

    print(heap.find_min())
    print(heap.extract_min())
    heap.insert({'name': 'Carlos', 'priority': 2})

    while not heap.is_empty():
        print(heap.extract_min())