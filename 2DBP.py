import random
import numpy as np
import draw


def item_fits(bin, item):
    return item <= len(bin[0]) and item <= len(bin)


def get_coordinates(bin, item):
    return random.randint(0, len(bin[0]) - item), random.randint(0, len(bin) - item)


def get_restricted_coordinates(bin, item):
    x = random.randint(0, len(bin[0]) - item)
    if x == 0 or x == len(bin[0] - item):
        y = random.randint(0, len(bin) - item)
    else:
        y = random.choice([0, len(bin) - item])
    return x, y


def partition_bins(bin, item, x, y):
    return [ bin[:y, :x], bin[:y, x:x + item], bin[:y, x + item:], bin[y:y + item, :x], bin[y:y + item, x + item:], \
           bin[y + item:, :x], bin[y + item:, x:x + item] , bin[y + item:, x + item:] ]


def add_item(bin, item, x, y, banned=False):
    for i in range(item):
        for j in range(item):
            bin[i+y][j+x] = -1 if banned else item
    return partition_bins(bin, item, x, y)


def add_bin_randomly(queue, bin):
    if random.uniform(0, 1) < .5:
        queue.append(bin)
    else:
        queue.insert(0, bin)


def update_queue(queue, bins):
    for bin in bins:
        if bin.size and bin[0].size:
            add_bin_randomly(queue, bin)


#TODO: Add code to check if contraband items fit in bin
#TODO: Add code to exit if item does not fit in any remaining bins
def add_banned_items(bin, banned):
    queue = [bin]
    while banned:
        curr_item = banned.pop(0)
        curr_bin = queue.pop(0)

        if not item_fits(curr_bin, curr_item):
            banned.insert(0, curr_item)
            queue.append(curr_bin)
            continue

        # generate initial position for item
        i, j = get_coordinates(curr_bin, curr_item)
        new_bins = add_item(curr_bin, curr_item, i, j, banned=True)
        for new_bin in new_bins:
            if new_bin.size and new_bin[0].size:
                add_bin_randomly(queue, new_bin)

    return queue


def fill_remaining_space(items, queue):
    while queue:
        curr_bin = queue.pop(0)
        for item in items:
            if item_fits(curr_bin, item):
                i, j = get_restricted_coordinates(curr_bin, item)
                new_bins = add_item(curr_bin, item, i, j)
                update_queue(queue, new_bins)
                break


def initialize_bin(dimensions):
    return np.array([[0 for _ in range(dimensions[0])] for _ in range(dimensions[1])])


def print_bin(bin):
    for row in bin:
        print(row)


def print_bin_statistics(size, bin):
    count = 0
    for row in bin:
        for value in row:
            if value == 0:
                count += 1

    fill_percent = (size[0] * size[1] - count) / (size[0] * size[1]) * 100

    print("Total Size: %d" % (size[0] * size[1]))
    print("Empty Boxes: %d" % count)
    print("Fill Percentage: %d" % fill_percent)

def main(size, banned, items):
    bin = initialize_bin(size)
    remaining_bins = add_banned_items(bin, banned)
    fill_remaining_space(items, remaining_bins)
    # print_bin(bin)
    print_bin_statistics(size, bin)
    draw.draw_2d_bin(bin)


# 2D example of bin packing, proof of concept, simplified without any rotations
# (i.e. we are only working with squares, filling a rectangular bin)
if __name__ == "__main__":
    bin_size = [20, 40]
    contraband = [4, 2, 1, 1, 1]
    remaining_items = [4, 3, 2]
    main(bin_size, contraband, remaining_items)
