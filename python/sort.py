import argparse
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# Generate an array with specific size.
def generate_array(array_size):
    array = []
    for i in range(array_size):
        array.append(random.randint(0, 5*array_size))
    return array

# Swap elements at position x and y of list A.
def swap(A, x, y):
    if x != y:
        A[x], A[y] = A[y], A[x]

# Sort the array |A| in ascending order.
# Bubble sort.
def bubble_sort(A):
    n = len(A)
    for i in range(n):
        for k in range(n-1, i, -1):
            if A[k] < A[k - 1]:
                swap(A, k, k-1)
            yield A

# Quick sort.
def quick_sort(A, low, high):
    if low >= high:
        return

    # Take last element as pivot, places the pivot element 
    # at its correct position in sorted array, and places 
    # all smaller (smaller than pivot) to left of pivot and 
    # all greater elements to right of pivot.
    pivot = A[high]
    pivotIdx = low
    for i in range(low, high):
        if A[i] < pivot:
            swap(A, i, pivotIdx)
            pivotIdx += 1
        yield A
    swap(A, high, pivotIdx)
    yield A

    # Continue sorting with the left and right part.
    yield from quick_sort(A, low, pivotIdx-1)
    yield from quick_sort(A, pivotIdx+1, high)

# Heap sort.
def heap_sort(A):
    def move_down(A, start, end):
        largest = 2*start + 1
        while largest <= end:
            # Right child exists and is larger than left child.
            if (largest < end) and (A[largest] < A[largest + 1]):
                largest += 1
        
            # Right child is larger than parent.
            if A[largest] > A[start]:
                swap(A, largest, start)
                # Move down to largest child.
                start = largest
                largest = 2 * start + 1
            else:
                return

    # Conver array to heap.
    length = len(A) - 1
    leastParent = length // 2
    for i in range(leastParent, -1, -1):
        move_down(A, i, length)
 
    # Flatten heap into sorted array.
    for i in range(length, 0, -1):
        if A[0] > A[i]:
            swap(A, 0, i)
            move_down(A, 0, i-1)
            yield A

# Merge sort.
def merge_sort(A, start, end):
    def merge(A, start, mid, end):
        merged = []
        leftIdx = start
        rightIdx = mid + 1

        while leftIdx <= mid and rightIdx <= end:
            if A[leftIdx] < A[rightIdx]:
                merged.append(A[leftIdx])
                leftIdx += 1
            else:
                merged.append(A[rightIdx])
                rightIdx += 1

        while leftIdx <= mid:
            merged.append(A[leftIdx])
            leftIdx += 1

        while rightIdx <= end:
            merged.append(A[rightIdx])
            rightIdx += 1

        for i, sorted_val in enumerate(merged):
            A[start + i] = sorted_val
            yield A

    if end <= start:
        return

    mid = start + ((end - start + 1) // 2) - 1
    yield from merge_sort(A, start, mid)
    yield from merge_sort(A, mid + 1, end)
    yield from merge(A, start, mid, end)
    yield A

# Main.
def main():
    # Initialize argparse and extract arguments. 
    parse = argparse.ArgumentParser()
    parse.add_argument('-as', '--array_size', type=int, default=20, help='Size of array which will be sorted')
    parse.add_argument('-st', '--sort_type', default='bubble', help='Sort type: bubble, quick, heap, merge')
    parse.add_argument('-i', '--interval', type=int, default=2, help='Interval time between 2 operations')
    parse.add_argument('-o', '--output', default='sort.gif', help='Output file name')
    parse.print_help()
    args = parse.parse_args()

    # Build a list of integers.
    A = generate_array(args.array_size)

    # Initialize |generator|, which is function pointer to sort funtions.
    if args.sort_type == 'bubble':
        generator = bubble_sort(A)
    elif args.sort_type == 'quick':
        generator = quick_sort(A, 0, len(A)-1)
    elif args.sort_type == 'heap':
        generator = heap_sort(A)
    elif args.sort_type == 'merge':
        generator = merge_sort(A, 0, len(A)-1)
    else:
        print('Unsupported sort type.')
        exit()

    # Initialize figure and axis.
    fig, ax = plt.subplots()
    ax.set_title('Sorting visualization: ' + args.sort_type + '_sort')

    # Initialize a bar plot.
    bar_rects = ax.bar(range(len(A)), A, align="edge")

    # Set axis limits.
    ax.set_xlim(0, len(A))
    ax.set_ylim(0, int(5.5 * len(A)))

    # Hide all the borders.
    # ax.axis('off')

    # Hide top and right borders.
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Hide the data in x and y axis.
    # ax.get_xaxis().set_visible(False)
    # ax.get_yaxis().set_visible(False)

    # Place a text label in the upper-left corner of the plot to display
    # number of operations performed by the sorting algorithm (each "yield"
    # is treated as 1 operation).
    text = ax.text(0.02, 0.95, "", transform=ax.transAxes)

    # Define function update_fig() for use with matplotlib.pyplot.FuncAnimation().
    iteration = [0]
    def update_fig(A, rects, iteration):
        for rect, val in zip(rects, A):
            rect.set_height(val)
        iteration[0] += 1
        text.set_text("# of operations: {}".format(iteration[0]))

    anim = animation.FuncAnimation(fig, func=update_fig,
        fargs=(bar_rects, iteration), frames=generator, interval=args.interval,
        repeat=False)
    
    # Save animation as gif.
    anim.save(args.output, dpi=80, writer='imagemagick')

    # Only show to desktop.
    # plt.show()

if __name__ == '__main__':
    main()