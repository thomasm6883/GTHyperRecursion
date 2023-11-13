import networkx as nx
import matplotlib.pyplot as plt
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

#increment the size of the graph using the scale,
def incrementGraph():
    global G, cases, node_positions, seed, node_color, labels
    G = nx.complete_graph(seed)#set the graph to the seed graph
    node_color = ['lightblue'] * len(G.nodes())
    print(G)
    x = 1
    while x < cases.get():#find the nth cartesian product
        print(x)
        #the second parameter will change when we allow user adjustment
        #m` = n*2^(n-1) or m2*n1+n2*m1 for cp
        #n' = 2^n for K2, but cartesian product is n1*n2
        G = nx.cartesian_product(G, nx.complete_graph(seed))
        node_color += ['lightblue'] * (2 ** x)
        x += 1
    node_positions = nx.circular_layout(G)
    update_plot()
#on the event of clicking a node, ensure that there is a node within the area to click and then set it. Find its index and set its color for user clarity
def on_node_click(event):
    global node_color, selected_node, node_positions, G
    if event.xdata is not None and event.ydata is not None:
        x, y = event.xdata, event.ydata
        for node, (nx, ny) in node_positions.items():
            if abs(x - nx) < 0.2 and abs(y - ny) < 0.2:
                selected_node = node

    #find the index
    index = 0
    for node in G:
        print(selected_node)
        print(node)
        if selected_node == node:
            break
        index+=1
    node_color[index] = 'red'
    update_plot()

#on the release of a node, change the coordinates and then change the color
def on_node_release(event):
    global selected_node, node_color, node_positions
    if selected_node is not None:
        x, y = event.xdata, event.ydata
        node_positions[selected_node] = (x, y)

        print(selected_node)

        #find the index
        index = 0
        for node in G:
            print(selected_node)
            print(node)
            if selected_node == node:
                break
            index += 1
        node_color[index] = 'lightblue'
        selected_node = None
        update_plot()

#update the plot by clearing the screen and redrawing
def update_plot():
    global G, node_color
    print("updating plot")
    ax.clear()
    nx.draw(G, pos=node_positions, with_labels=True, node_size=1010, node_color=node_color)
    canvas.draw()

selected_node = None

# Create the window for your project
root = Tk()
root.wm_title("Hyper-iority")

# Create a figure and axis for your NetworkX graph
fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111)

cases=IntVar()
cases.set(1)
seed = 2
G = nx.complete_graph(seed)
node_positions = nx.circular_layout(G)
node_color=['lightblue']*len(G.nodes)


nx.draw(G, pos=node_positions, with_labels=True, node_size=1010, node_color=node_color)

# Create a Tkinter canvas to embed the Matplotlib figure
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=TOP, fill=BOTH, expand=True)

# Add a Matplotlib navigation toolbar (optional)
toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas_widget.pack(side=TOP, fill=BOTH, expand=True)

#add an incremental scale: label here
scaleLabel = Label(root, text="Increment Recursive Cases")
scaleLabel.pack()
#scale here
recursiveCases = Scale(root, variable=cases, from_=1, to=4, orient=HORIZONTAL, command=lambda val:incrementGraph())
recursiveCases.pack(anchor = CENTER)

#add listeners for node clicks
canvas.mpl_connect('button_press_event', on_node_click)
canvas.mpl_connect('button_release_event', on_node_release)

# Main loop to run the Tkinter application
root.mainloop()
