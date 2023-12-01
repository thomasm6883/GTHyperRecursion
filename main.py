import networkx as nx
import matplotlib.pyplot as plt
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

#increment the size of the graph using the scale,
def incrementGraph():
    global G, cases, node_positions, seed, node_color, seedGraph, newGraph
    if (newGraph==False):
        G = seedGraph#set the graph to the seed graph
        node_color = ['lightblue'] * len(G.nodes())
        x = 1
        while x < cases.get():#find the nth cartesian product
            node_color = ['lightblue'] * (len(G.nodes()) * len(seedGraph.nodes()))
            G = nx.cartesian_product(G, seedGraph)

            x += 1
        node_positions = nx.shell_layout(G)
        update_plot()

#on the event of clicking a node, ensure that there is a node within the area to click and then set it.
# node_positions = nx.circular_layout(G)
#Find its index and set its color for user clarity
def on_node_click(event):
    global node_color, selected_node, node_positions, G
    if event.xdata is not None and event.ydata is not None:
        x, y = event.xdata, event.ydata
        for node, (nx, ny) in node_positions.items():
            if abs(x - nx) < 0.02 and abs(y - ny) < 0.02:
                selected_node = node

    #find the index
    index = 0
    for node in G:
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

        #find the index
        index = 0
        for node in G:
            if selected_node == node:
                break
            index += 1
        node_color[index] = 'lightblue'
        selected_node = None
        update_plot()

#update the plot by clearing the screen and redrawing
def update_plot():
    global G, node_color
    ax.clear()
    nx.draw(G, pos=node_positions, with_labels=TRUE, node_size=20, node_color=node_color)
    canvas.draw()

def addNodeToGraph():
    global G, cases, node_positions, node_color, seedGraph, newGraph, numNodes
    if (newGraph==False):
        node_color = []
        #TODO - change what node_positions is here
        node_positions = nx.shell_layout(nx.complete_graph(2))
        seedGraph.clear()
        cases.set(1)
        update_plot()
        newGraph = True
    if (numNodes < 8):
        seedGraph.add_node(numNodes)
        node_color += ['lightblue']

    G = seedGraph
    numNodes+=1
    node_positions = nx.shell_layout(G)
    update_plot()

def submitGraph():
    global newGraph
    newGraph = False

def addEdgeA_B():
    global G, seedGraph, addEdgeInputB, addEdgeInputA, newGraph
    if (newGraph):
        seedGraph.add_edge(int(addEdgeInputA.get()), int(addEdgeInputB.get()))
        G = seedGraph
        update_plot()

def clearGraph():
    global G, cases, node_positions, node_color, seedGraph, newGraph, numNodes
    numNodes=2
    # TODO - change what node_positions is here
    G=nx.complete_graph(2)
    seedGraph.clear()
    seedGraph = G
    node_positions = nx.shell_layout(G)
    node_color = ['lightblue']*len(G.nodes)
    cases.set(1)
    update_plot()
    newGraph = True
    update_plot()

def convertTuple(tup):
    returnStr = ''
    count = 1
    if isinstance(tup, int):
        return '(' + returnStr + ')'
    for node in tup:
        if isinstance(node, tuple):
            returnStr += convertTuple(node)
        else :
            returnStr += str(node)
        if count < 2:
            returnStr+= ', '
        count+=1
    return '(' + returnStr + ')'
def findAvailable(pSize, currVertex, listAvailable):
    for edge in pSize:
        if (edge != 'x'):
            if (edge[0] == currVertex):
                listAvailable.append(edge[1])
            elif (edge[1] == currVertex):
                listAvailable.append(edge[0])
    if (len(listAvailable) > 0):
        return len(listAvailable)
    else: return -1

def constructEdge(vertex1, vertex2, pSize):
    edgeA = '(' + convertTuple(vertex1) + ', ' + convertTuple(vertex2) + ')'
    edgeB = '(' + convertTuple(vertex2) + ', ' + convertTuple(vertex1) + ')'

    for edge in pSize:
        if (edge == 'x'): continue
        edgeC = convertTuple(edge)
        if (edgeA == edgeC or edgeB == edgeC):
            return edge
    return -1

def showEulerian():
    global node_positions, G
    availablePaths = TRUE
    P = G
    #the list of all edges in G, copied in P
    pSize = list(P.edges)
    if (len(pSize) > 1000):
        print('Thats pretty big, idk about that')
        return
    # the list of all Nodes in G, copied in P
    pOrder = list(P.nodes)
    EulerianStack = []

    EulerianStack.append(pOrder[0])
    #print(EulerianStack[-1])
    #print(len(pSize))
    EulerianStack = findEulerian(pSize, EulerianStack, len(pSize))
    count = 1
    formattedStack = ''
    if EulerianStack:
        for node in EulerianStack:
            formattedStack += convertTuple(node) + ' -> '
            if (count % 5 == 0):
                print(formattedStack)
                formattedStack = ''
            count += 1
            if count == len(EulerianStack):
                print(formattedStack)
    else:
        print('Not Eulerian!')
def checkNone(pSize):
    for edge in pSize:
        if edge != 'x':
            return False
    return True
def findEulerian(pSize, EulerianStack, goalN):
    #print('New Iteration: Here\'s pSize')
    #print(pSize)
    if (checkNone(pSize)):
        if (len(EulerianStack)-1 == goalN): return EulerianStack
        else: return False
    else:
        listAvailable = []
        findAvailable(pSize, EulerianStack[-1], listAvailable)
        #print('Available: ')
        #print(listAvailable)
        for node in listAvailable:
            #print('(' + convertTuple(EulerianStack[-1]) + ', ' + convertTuple(node) + ')')
            edgeToReplace = constructEdge(EulerianStack[-1], node, pSize)
            #print('Next edge to be removed')
            #print(edgeToReplace)
            if (edgeToReplace != -1):
                EulerianStack.append(node)
                i = 0
                for edge in pSize:
                    if (edge == edgeToReplace):
                        replaceNode = i
                        #print('replaced')
                    i+=1
                pSize[replaceNode] = 'x'
                #print('Stack')
                #print(EulerianStack)
                if (findEulerian(pSize, EulerianStack, goalN)):return EulerianStack
                else:
                    EulerianStack.pop()
                    pSize[replaceNode] = edgeToReplace

def showHamiltonian():
    global node_positions, G
    if (len(node_positions) > 0):
        for node, (nx, ny) in node_positions.items():
            print(node)
#=================================================================
selected_node = None

newGraph = FALSE
numNodes = 0

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
seedGraph = G
node_positions = nx.shell_layout(G)
node_color=['lightblue']*len(G.nodes)

#draw default graph defined above
nx.draw(G, pos=node_positions, with_labels=TRUE, node_size=10, node_color=node_color)


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

#add a button to add nodes : these will not yet be recursed, so label them A-Z, don't allow any more
#on this button click, set a boolean to clear the Graph and window and then start adding nodes if the boolean is false
addNodesButton = Button(root, text="Add Node", command=lambda:addNodeToGraph())
addNodesButton.pack(side=LEFT)

#add a text selection to add edges between nodes
edgeTextLabel = Label(root, text="Add Edges")
edgeTextLabel.pack(side=LEFT)
edgeTextLabelA = Label(root, text="A: ")
edgeTextLabelA.pack(side=LEFT)
addEdgeInputA = Entry(root)
addEdgeInputA.pack(side=LEFT)
edgeTextLabelB = Label(root, text="B: ")
edgeTextLabelB.pack(side=LEFT)
addEdgeInputB = Entry(root)
addEdgeInputB.pack(side=LEFT)
submitEdgesButton = Button(root, text="Submit A & B", command=lambda:addEdgeA_B())
submitEdgesButton.pack(side=LEFT)

#add a button to 'submit' G
submitGraphButton = Button(root, text="Submit Graph", command=lambda:submitGraph())
submitGraphButton.pack(side=BOTTOM)

clearGraphButton = Button(root, text="Clear Graph", command=lambda:clearGraph())
clearGraphButton.pack(side=BOTTOM)

#extra functions
eulerianDetection = Button(root, text="Print Eulerian If Existent", command=lambda:showEulerian())
eulerianDetection.pack(side=BOTTOM)

#add listeners for node clicks
canvas.mpl_connect('button_press_event', on_node_click)
canvas.mpl_connect('button_release_event', on_node_release)

# Main loop to run the Tkinter application
root.mainloop()
