#notes for changing back to heapq
    #uncomment out the import
    # change every open_list length check back from len(open_list.heap) to len(open_list)
    # change every open_list.heap[0][0] back to open_list[0][0]
    # change the lines after the if in check_and_remove back to just open_list.remove(tuple)
    # in heap_insert, change open_list.insert(tuple) back to hq.heappush(open_list, tuple)


#implementation of BinaryHeap
    # ONLY TAKES TUPLES/LISTS AS ELEMENTS because thats what we need for this project
class BinaryHeap:
    def __init__(self):
        self.heap = []

    #return position of a node's parent in the heap
    def get_parent(self, pos):
        return int(pos/2)

    #swaps the positions of two nodes in the heap
    def swap(self,parent_pos, child_pos):
        temp = self.heap[parent_pos]
        self.heap[parent_pos] = self.heap[child_pos]
        self.heap[child_pos] = temp
        return parent_pos
    
    #compares the values of two entries in the heap. Our entries are always tuples, so compares their entries
    def compare(self, a, b):
        for i in range(min(len(a), len(b))):
            if a[i] != b[i]:
                return a[i]-b[i]
        return 0

    #determines whether a node has children. when reheaping, we stop if the node we are at doesn't have any children
    def hasChildren(self, pos):
        if pos < len(self.heap) and pos > int(len(self.heap)/2):
            return False
        return True

    #fix the heap after removing an item from it
    def reheap(self, cur):
        if self.hasChildren(cur):
            #check left child
            if 2*cur < len(self.heap):
                if self.compare(self.heap[cur],self.heap[2*cur])>0:
                    self.swap(cur, 2*cur)
                    self.reheap(2*cur)
            #check right child
            if 2*cur+1 < len(self.heap):
                if self.compare(self.heap[cur], self.heap[2*cur+1])>0:
                    self.swap(cur, 2*cur+1)
                    self.reheap(2*cur+1)


        return

    #add new item into the heap
    def insert(self, new_val):
        self.heap.append(new_val)
        pos = len(self.heap)-1
        while self.compare(self.heap[self.get_parent(pos)] , self.heap[pos]) > 0:
            pos = self.swap(self.get_parent(pos), pos)

    #remove the first value from the heap
    def pop(self):
        ret = self.heap[0]
        self.heap = self.heap[1:]
        self.reheap(0)
        return ret





    