from BinaryHeap import BinaryHeap 
def main():
    heap = BinaryHeap()
    heap.insert([2])
    heap.insert([5])
    heap.insert([7])
    heap.insert([8])
    heap.insert([10])
    heap.insert([9])
    ret = heap.pop()
    heap.pop()
    heap.pop()
    heap.pop()
    for i in heap.heap:
        print(i)
    #print(heap)
    return

if __name__ == "__main__":
    main()