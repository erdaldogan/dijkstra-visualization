from tkinter import *
from dijkstra import Graph
from tkinter import font  as tkfont
import time

black = (0, 0, 0)
linewidth = 5
white = (255, 255, 255)
radius = 0
graph = None
time_elapsed = 0
root = Tk()
frame = Frame(root, width="1000", height="550")
frame.grid(row=0, column=0)
root.configure(background='#EFEFEF')
root.title("Dijkstra Visualization")

algorithm_font = tkfont.Font(family='Helvetica', size=30, weight="bold", slant="italic")
Label(frame, text="Dijkstra Visualization", font=algorithm_font).grid(row=0, column=0)

canvas = Canvas(frame, width="1000", height="500", bd="1", relief='raised', scrollregion=(0, 0, 100000, 0))
canvas.grid(row=6, column=0, rowspan=1)
canvas.configure(scrollregion=canvas.bbox("all"))

hbar = Scrollbar(frame, orient=HORIZONTAL, activebackground="black")
hbar.grid(row=7, columnspan=6, sticky='ew')
hbar.config(command=canvas.xview)
canvas.config(xscrollcommand=hbar.set)

path_frame = Frame(frame)
path_frame.grid(row=5, column=0)

path_var = StringVar(value="")
path_entry = Entry(path_frame, textvariable=path_var, state='readonly', width=100)
path_entry.grid(row=3, column=0)

path_hbar = Scrollbar(path_frame, orient=HORIZONTAL, activebackground="black", command=path_entry.xview)
path_hbar.grid(row=6, column=0, sticky='ew')
path_hbar.config(command=path_entry.xview)
path_entry.config(xscrollcommand=path_hbar.set)

running_time_weight_frame = Frame(frame)
running_time_weight_frame.grid(row=3, column=0)

running_time = StringVar(value="Running Time: 0ms")
running_time_label = Label(running_time_weight_frame, textvariable=running_time)
running_time_label.grid(row=0, column=0, columnspan=2, padx=(10, 100))

weight_var = StringVar(value="Total Weight of Path: 0")
weight_label = Label(running_time_weight_frame, textvariable=weight_var)
weight_label.grid(row=0, column=3, padx=(100, 10))


def calculate_radius():
    global radius
    radius = 50 + (int(number_of_elements.get())) / int(number_of_elements.get())


def add_vertex(data, x1, y1):
    try:
        x2, y2 = (x1 + radius), (y1 + radius)
        canvas.create_oval(x1, y1, x2, y2, fill="#FFF", outline="black")
        canvas.create_text(x1 + radius // 2, y1 + radius // 2, text=str(data))

    except Exception as e:
        print(e)


def add_v_edge(x1, x2, y1, y2, pos=1):
    try:
        x1 = x2 = x1 + radius / 2
        y1 = y1 + radius
        if pos == 2:
            canvas.create_line(x1, y1, x2, y2, fill="#ff0000", width=linewidth)
            return None

        canvas.create_line(x1, y1, x2, y2, fill="#000")

    except Exception as e:
        print(e)


def add_h_edge(x1, x2, y1, y2, pos=0):  # pos = 1: only upper edge; else both edge
    try:
        if pos == 2:
            canvas.create_line(x1 - (2 * radius), y1 + radius // 2, x1, y1 + radius // 2, fill="#ff0000",
                               width=linewidth)
            return None

        canvas.create_line(x1 - (2 * radius), y1 + radius // 2, x1, y1 + radius // 2, fill="#000")
        if pos != 1:
            canvas.create_line(x2 - (2 * radius), y2 + radius // 2, x2, y2 + radius // 2, fill="#000")

    except Exception as e:
        print(e)


def add_d_edge(x1, y1, pos=0):  # pos = 1: only upper edge; else both edge
    gap = (radius * pow(2, 0.5)) - radius
    xp = yp = gap / pow(2, 0.5)
    try:
        if pos == 2:
            canvas.create_line(x1 - (2 * radius) - xp / 2, (y1 + 3 * radius) + yp / 2, x1 + xp / 2,
                               y1 + radius - yp / 2, fill="#ff0000", width=linewidth)
            return None

        elif pos == 3:
            canvas.create_line(x1 - (2 * radius) - xp / 2, y1 + radius - yp / 2, x1 + xp / 2,
                               (y1 + 3 * radius) + yp / 2, fill="#ff0000", width=linewidth)
            return None

        canvas.create_line(x1 - (2 * radius) - xp / 2, (y1 + 3 * radius) + yp / 2, x1 + xp / 2, y1 + radius - yp / 2,
                           fill="#000")
        if pos != 1:
            canvas.create_line(x1 - (2 * radius) - xp / 2, y1 + radius - yp / 2, x1 + xp / 2,
                               (y1 + 3 * radius) + yp / 2, fill="#000")

    except Exception as e:
        print(e)


def create_graph(number_of_elements):
    global graph
    graph = Graph(number_of_elements)
    for i in range(1, number_of_elements):
        for j in range(i, number_of_elements + 1):
            if i % 2 == 1:
                if max(i - j, j - i) <= 3 and i != j:
                    graph.add_edge(i, j)
            else:
                if max(i - j, j - i) <= 2 and i != j:
                    graph.add_edge(i, j)
    start = time.time()
    (path_output, weight_output) = graph.dijkstra_shortest_path(int(from_entry.get()), int(to_entry.get()))
    end = time.time()
    visualize_shortest_path(path_output)
    print("output ", path_output[::-1])
    print("time ", end - start)
    running_time.set("Running Time:" + str("{0:.2f}".format(round((end - start) * 1000, 2))) + "ms")
    string = "Path: "
    for i in range(len(path_output[::-1]) - 1): string += str(path_output[::-1][i]) + " -> "
    path_var.set(string + str(path_output[::-1][len(path_output) - 1]))
    weight_var.set("Total Weight: " + str(weight_output))
    print(graph.dijkstra_shortest_path_distances(int(to_entry.get())))


def visualize_shortest_path(path):
    for i in range(len(path) - 1):
        current_node = path[i]
        next_node = path[i + 1]
        if (current_node % 2 == 0 and next_node == current_node - 1) or (current_node % 2 == 1
                                                                         and next_node == current_node + 1):
            x1 = x2 = 100 + (min(current_node, next_node) - 1) / 2 * radius * 3
            y1, y2 = (500 - 7 * radius), (500 - 7 * radius) + (radius * 3)
            add_v_edge(x1, x2, y1, y2, 2)

        elif current_node % 2 == 0 and next_node % 2 == 1:
            if next_node > current_node:
                x1 = 253 + abs(current_node / 2 - 1) * 153
                y1, y2 = (500 - 7 * radius), (500 - 7 * radius) + (radius * 3)
                add_d_edge(x1, y1, 2)
            elif next_node < current_node:
                x1 = 253 + (next_node - 1) / 2 * 153
                y1, y2 = (500 - 7 * radius), (500 - 7 * radius) + (radius * 3)
                add_d_edge(x1, y1, 3)
        elif current_node % 2 == 1 and next_node % 2 == 0:
            if next_node > current_node:
                x1 = 253 + abs(next_node / 2 - 2) * 153
                y1, y2 = (500 - 7 * radius), (500 - 7 * radius) + (radius * 3)
                add_d_edge(x1, y1, 3)
            elif next_node < current_node:
                x1 = 253 + (current_node - 3) / 2 * 153
                y1, y2 = (500 - 7 * radius), (500 - 7 * radius) + (radius * 3)
                add_d_edge(x1, y1, 2)
        elif current_node % 2 == next_node % 2:
            if current_node % 2 == 1:
                x1 = x2 = 100 + radius * 3 * (max(current_node, next_node) - 1) / 2
                y1, y2 = (500 - 7 * radius), (500 - 7 * radius) + (radius * 3)
            else:
                x1 = x2 = 100 + radius * 3 * min(current_node, next_node) / 2
                y1, y2 = (500 - 7 * radius) + 3 * radius, (500 - 7 * radius) + (radius * 6)
            add_h_edge(x1, x2, y1, y2, 2)


def run_program():
    global canvas
    canvas.delete("all")
    calculate_radius()
    noe = int(number_of_elements.get())
    canvas.configure(scrollregion=(0, 0, 100 + noe * 78, 0))
    x1 = x2 = 100
    counter = 1
    y1, y2 = (500 - 7 * radius), (500 - 7 * radius) + (radius * 3)
    for i in range(noe // 2):
        add_vertex(counter, x1, y1)
        add_vertex(counter + 1, x2, y2)
        add_v_edge(x1, x2, y1, y2)
        counter += 2
        if counter - 1 > 2 and (counter - 1) % 2 == 0:
            add_h_edge(x1, x2, y1, y2)
            add_d_edge(x1, y1)

        x1 = x2 = 100 + radius * 3 * (i + 1)
    if noe % 2 == 1:
        add_vertex(noe, x1, y1)
        add_h_edge(x1, x2, y1, y2, 1)
        add_d_edge(x1, y1, 1)
    create_graph(noe)


from_frame = Frame(frame)
from_frame.grid(row=1, column=0)

number_of_elements = Entry(from_frame)
number_of_elements.grid(row=1, column=0)
number_of_elements.insert(0, "Number of Elements")
number_of_elements.configure(state=DISABLED)


def on_click_from_noe(event):
    number_of_elements.configure(state=NORMAL)
    number_of_elements.delete(0, END)
    number_of_elements.unbind('<Button-1>', on_click_id_noe)


on_click_id_noe = number_of_elements.bind('<Button-1>', on_click_from_noe)

from_entry = Entry(from_frame)
from_entry.grid(row=1, column=1)
from_entry.insert(0, "From")
from_entry.configure(state=DISABLED)


def on_click_from_entry(event):
    from_entry.configure(state=NORMAL)
    from_entry.delete(0, END)
    from_entry.unbind('<Button-1>', on_click_id_from)


on_click_id_from = from_entry.bind('<Button-1>', on_click_from_entry)

to_entry = Entry(from_frame)
to_entry.grid(row=1, column=2)
to_entry.insert(0, "To")
to_entry.configure(state=DISABLED)


def on_click_to_entry(event):
    to_entry.configure(state=NORMAL)
    to_entry.delete(0, END)
    to_entry.unbind('<Button-1>', on_click_id_to)


on_click_id_to = to_entry.bind('<Button-1>', on_click_to_entry)

from_entry_button = Button(from_frame, text='Set From and To', command=lambda: run_program())
from_entry_button.grid(row=1, column=3, columnspan=1)

root.mainloop()
