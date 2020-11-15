"""
Main file for the gui.
"""

import tkinter as tk
from tkinter import ttk
import tab_maker as tm
from inspect import signature  # getting the number of params in a function
import M_M_s
import mmsk
import M_D_1
import M_Ek_1
import M_G_1
import M_M_1

# Frame
window = tk.Tk()
window.title("Queue Simulator")
window.geometry("1000x1000")
parent_tab = ttk.Notebook(window)

s = ttk.Style()
s.configure('TFrame', background=tm.BASE_COL)

##### M/M/s TAB ###############
sig_mms = signature(M_M_s.mms)
mms_params = sig_mms.parameters
tm.make_mms_tab(parent_tab, len(mms_params))

#####  M/M/s/k  TAB   ###############
sig_mmsk = signature(mmsk.get_mmsk)
mmsk_params = sig_mmsk.parameters
tm.make_mmsk_tab(parent_tab, len(mmsk_params))

# ################################################ M/G/1 TAB ###################################################
sig_mg1 = signature(M_G_1.get_m_g_1)
mg1_params = sig_mg1.parameters

tm.make_mg1_tab(parent_tab, len(mg1_params))

# ############################################## M/D/1 TAB ####################################################
sig_md1 = signature(M_D_1.get_m_d_1)
md1_params = sig_md1.parameters

tm.make_md1_tab(parent_tab, len(md1_params))

# ############################################# M/Ek/1 TAB ####################################################
sig_mek1 = signature(M_Ek_1.get_m_ek_1)
mek1_params = sig_mek1.parameters

tm.make_mek1_tab(parent_tab, len(mek1_params))

# adding all tabs to the window
parent_tab.pack(expand=1, fill="both")

window.mainloop()
