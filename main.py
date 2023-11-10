import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

def on_node_click(event):
    if event.xdata is not None and event.ydata is not None:
        x, y = event.xdata, event.ydata
        for node, (nx, ny) in node_positions.items():
            if abs(x - nx) < 0.02 and abs(y - ny) < 0.02:
                global selected_node
                selected_node = node

def on_node_release(event):
    if selected_node is not None:
        x, y = event.xdata, event.ydata
        node_positions[selected_node] = (x, y)
        update_plot()

def update_plot():
    ax.clear()
    nx.draw(G, pos=node_positions, with_labels=True, node_size=3000, node_color='lightblue')
    canvas.draw()

selected_node = None

# Create the window for your project
root = tk.Tk()
root.wm_title("Hyper-iority")

# Create a figure and axis for your NetworkX graph
fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111)

x = 0
seed = 2
G = nx.complete_graph(seed)
while x < 3:
    G = nx.cartesian_product(G, nx.complete_graph(seed))
    x = x + 1
    print(x)

# Plot the NetworkX graph on the Matplotlib figure
node_positions = nx.circular_layout(G)
nx.draw(G,node_positions, ax=ax)

# Create a Tkinter canvas to embed the Matplotlib figure
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Add a Matplotlib navigation toolbar (optional)
toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

canvas.mpl_connect('button_press_event', on_node_click)
canvas.mpl_connect('button_release_event', on_node_release)

# Main loop to run the Tkinter application
tk.mainloop()
