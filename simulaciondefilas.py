import tkinter as tk
from tkinter import ttk
import tab_maker as tm

# Frame
window = tk.Tk()
window.title("Queue Simulator")
window.geometry("1000x1000")
parent_tab = ttk.Notebook(window)

s = ttk.Style()
s.configure('TFrame', background=tm.BASE_COL)

############################################ M/M/s TAB #######################################################

tm.make_mms_tab(parent_tab)

######################################################  M/M/s/k  TAB   ###########################################################

tm.make_mmsk_tab(parent_tab)

# ################################################ M/G/1 TAB ###################################################

tm.make_mg1_tab(parent_tab)

# ############################################## M/D/1 TAB ####################################################

tm.make_md1_tab(parent_tab)

# ############################################# M/Ek/1 TAB ####################################################

tm.make_mek1_tab(parent_tab)

# adding all tabs to the window
parent_tab.pack(expand=1, fill="both")

window.mainloop()
