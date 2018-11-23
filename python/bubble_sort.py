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
def bubble_sort(A):
    n = len(A)
    for i in range(n):
        for k in range(n - 1, i, -1):
            if A[k] < A[k - 1]:
                swap(A, k, k - 1)
            yield A

# Main.
def main():
    # Build a list of integers.
    A = generate_array(50)

    # Initialize figure and axis.
    fig, ax = plt.subplots()
    ax.set_title("Bubble sort")

    # Initialize a bar plot.
    bar_rects = ax.bar(range(len(A)), A, align="edge")

    # Set axis limits.
    ax.set_xlim(0, len(A))
    ax.set_ylim(0, int(5 * len(A)))

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
        fargs=(bar_rects, iteration), frames=bubble_sort(A), interval=500,
        repeat=False)
    
    # Save animation as gif.
    anim.save('sort.gif', dpi=80, writer='imagemagick')

    # Only show to desktop.
    # plt.show()

if __name__ == '__main__':
    main()