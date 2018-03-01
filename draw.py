import matplotlib.pyplot as plt


def draw_2d_bin(bin):
    fig, ax = plt.subplots()

    ax.imshow(bin, cmap=plt.cm.RdYlBu, interpolation='nearest')
    plt.show()
