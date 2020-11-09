import tkinter as tk
from tkinter import ttk
from tkinter import Entry, messagebox
from enum import Enum

from wx.core import TEXT_ATTR_EFFECT_CAPITALS

import M_M_s as mms
import mmsk
import M_D_1 as md1
import M_Ek_1 as mek1
import M_G_1 as mg1

HEIGHT = 900
WIDTH = 900

class Model(Enum):
    MD1 = 1
    MEK1 = 2
    MG1 = 3
    MMS = 4
    MMSK = 5

## Handler functions
def get_results(model, input_list):
    """
    Receives the input list from the form
    specifically:
    s - servers
    l - lambda
    m - miu
    k - (optional) expected customers
    sigma - (optional) std deviation
    """
    if not input_list:
        messagebox.showerror("Error", "No input detected")
    else:
        try:
            s = int(input_list[0])
            l = int(input_list[1])
            m = int(input_list[2])
        except ValueError as verr:
            messagebox.showerror("Error", verr)
        else:
            res = {}
            if model == Model.MMS:
                n = 1 #TODO unhardcode this
                res = mms.mms(l, m, n, s)
            elif model == Model.MMSK:
                k = int(input_list[3]) #TODO unhardcode this
                res = mmsk.get_mmsk(l, m, s, k)

            build_report_win(res)

def build_report_win(res):
    """
    Function to build result window
    res - Dictionary
    """
    res_win = tk.Tk()
    res_win.title("Results")
    canvas = tk.Canvas(res_win, height=HEIGHT/2, width=WIDTH/2)
    canvas.pack()
    resframe = tk.Frame(master=res_win, bg=BASE_COL)
    resframe.place(relheight=1, relwidth=1)
    num_res = len(res)
    i=0

    for key, value in res.items():
        tk.Label(master=resframe, text=key, font=55, bg=BASE_COL, foreground=TEXT_COL).place(relwidth=0.1, relheight=1/num_res, rely=i/num_res)
        tk.Label(master=resframe, text=str(value), font=55, bg=BASE_COL, foreground=TEXT_COL).place(relwidth=0.45, relheight=1/num_res, relx=0.15, rely=i/num_res)
        i += 1


## base vals
BASE_COL = "#303030"
TEXT_COL = "#dcdcdc"

###Frame
window = tk.Tk()
window.title("Queue Simulator")
window.geometry("900x900")
parent_tab = ttk.Notebook(window)

s = ttk.Style()
s.configure('TFrame', background=BASE_COL)

mms_tab = ttk.Frame(master=parent_tab, style='TFrame')
##The number of servers
s_frame = ttk.Frame(master=mms_tab)
s_frame.place(relwidth=1, relheight=1/3)

s_label = ttk.Label(master=s_frame, text="Number of servers (s)", font=45, background=BASE_COL, foreground=TEXT_COL)
s_label.place(relx=0, rely=0, relheight=0.15, relwidth=0.25)
s_entry = tk.Entry(master=s_frame, font=45)
s_entry.insert(0, "1")
s_entry.place(relx=0.3, rely=0.05, relheight=0.1, relwidth=0.25)
s_description = tk.Label(master=s_frame, text="\tThe number of servers denotes how many clients can be dealt with simultaneously.\nAugmenting servers can affect cost.", 
fg=TEXT_COL, bg=BASE_COL, anchor="w", font=50)
s_description.place(relx=0, rely=0.3)

#Lambda
l_frame = ttk.Frame(master=mms_tab)
l_frame.place(relwidth=1, relheight=1/3, rely=1/3)

l_label = ttk.Label(master=l_frame, text="Frequence of service" + u" \u03bb", font=45, background=BASE_COL, foreground=TEXT_COL)
l_label.place(relx=0, rely=0, relheight=0.15, relwidth=0.25)
l_entry = tk.Entry(master=l_frame, font=45)
l_entry.insert(0, u"\u03bb")
l_entry.place(relx=0.3, rely=0.05, relheight=0.1, relwidth=0.25)
l_description = tk.Label(master=l_frame, text="\tThe number of servers denotes how many clients can be dealt with simultaneously.\nAugmenting servers can affect cost.", 
foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=50)
l_description.place(relx=0, rely=0.3)

##Miu
m_frame = ttk.Frame(master=mms_tab)
m_frame.place(relwidth=1, relheight=1/3, rely=2/3)

m_label = ttk.Label(master=m_frame, text="Service frequence"+ u" \u03bc", font=45, background=BASE_COL, foreground=TEXT_COL)
m_label.place(relx=0, rely=0, relheight=0.15, relwidth=0.25)
m_entry = tk.Entry(master=m_frame, font=45)
m_entry.insert(0,u"\u03bc")
m_entry.place(relx=0.3, rely=0.05, relheight=0.1, relwidth=0.25)
m_description = tk.Label(master=m_frame, text="\tThe number of servers denotes how many clients can be dealt with simultaneously.\nAugmenting servers can affect cost.", 
foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=50)
m_description.place(relx=0, rely=0.3)

ok_btn = tk.Button(master=m_frame, text="OK", anchor="c", command=lambda: get_results(Model.MMS, [s_entry.get(), l_entry.get(), m_entry.get()]))
ok_btn.place(relx=0.40, rely=0.7, relheight=0.1, relwidth=0.2)

parent_tab.add(mms_tab, text="M/M/s")

######################################################   TAB 2      ###############################################################
mmsk_tab = ttk.Frame(master=parent_tab, style='TFrame')
##The number of servers
s_frame = ttk.Frame(master=mmsk_tab)
s_frame.place(relwidth=1, relheight=1/4)

s_label = ttk.Label(master=s_frame, text="Number of servers (s)", font=45, background=BASE_COL, foreground=TEXT_COL)
s_label.place(relx=0, rely=0, relheight=0.15, relwidth=0.25)
s_entry = tk.Entry(master=s_frame, font=45)
s_entry.insert(0, "1")
s_entry.place(relx=0.3, rely=0.05, relheight=0.1, relwidth=0.25)
s_description = tk.Label(master=s_frame, text="\tThe number of servers denotes how many clients can be dealt with simultaneously.\nAugmenting servers can affect cost.", 
fg=TEXT_COL, bg=BASE_COL, anchor="w", font=50)
s_description.place(relx=0, rely=0.3)

#Lambda
l_frame = ttk.Frame(master=mmsk_tab)
l_frame.place(relwidth=1, relheight=1/4, rely=1/4)

l_label = ttk.Label(master=l_frame, text="Frequence of service" + u" \u03bb", font=45, background=BASE_COL, foreground=TEXT_COL)
l_label.place(relx=0, rely=0, relheight=0.15, relwidth=0.25)
l_entry = tk.Entry(master=l_frame, font=45)
l_entry.insert(0, u"\u03bb")
l_entry.place(relx=0.3, rely=0.05, relheight=0.1, relwidth=0.25)
l_description = tk.Label(master=l_frame, text="\tThe number of servers denotes how many clients can be dealt with simultaneously.\nAugmenting servers can affect cost.", 
foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=50)
l_description.place(relx=0, rely=0.3)

##Miu
m_frame = ttk.Frame(master=mmsk_tab)
m_frame.place(relwidth=1, relheight=1/4, rely=2/4)

m_label = ttk.Label(master=m_frame, text="Service frequence"+ u" \u03bc", font=45, background=BASE_COL, foreground=TEXT_COL)
m_label.place(relx=0, rely=0, relheight=0.15, relwidth=0.25)
m_entry = tk.Entry(master=m_frame, font=45)
m_entry.insert(0,u"\u03bc")
m_entry.place(relx=0.3, rely=0.05, relheight=0.1, relwidth=0.25)
m_description = tk.Label(master=m_frame, text="\tThe number of servers denotes how many clients can be dealt with simultaneously.\nAugmenting servers can affect cost.", 
foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=50)
m_description.place(relx=0, rely=0.3)

##Expoected customers k
k_frame = ttk.Frame(master=mmsk_tab)
k_frame.place(relwidth=1, relheight=1/4, rely=4/5)

k_label = tk.Label(master=k_frame, text="Number of expected customers", bg=BASE_COL, foreground=TEXT_COL, font=45)
k_label.place(relx=0, rely=0, relheight=0.15, relwidth=0.3)
k_entry = tk.Entry(master=k_frame, font=45)
k_entry.insert(0, "k")
k_entry.place(relx=0.3, rely=0.05, relheight=0.1, relwidth=0.25)
k_description = tk.Label(master=k_frame, text="\tk allows to know how many customers to expect into the system.\nIf not applicable, use the M/M/s tab.", 
foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=50)
k_description.place(relx=0, rely=0.3)


ok_btn = tk.Button(master=k_frame, text="OK", anchor="c", command=lambda: get_results(Model.MMSK, [s_entry.get(), l_entry.get(), m_entry.get(), k_entry.get()]))
ok_btn.place(relx=0.40, rely=0.65, relheight=0.1, relwidth=0.2)
parent_tab.add(mmsk_tab, text="M/M/s/k")

mg1_tab = ttk.Frame(master=parent_tab, style='TFrame')
parent_tab.add(mg1_tab, text="M/G/1")

md1_tab = ttk.Frame(master=parent_tab, style='TFrame')
parent_tab.add(md1_tab, text="M/D/1")

mek1_tab = ttk.Frame(master=parent_tab, style='TFrame')
parent_tab.add(mek1_tab, text="M/Ek/1")

parent_tab.pack(expand=1, fill="both")



# ##The number of servers
# s_frame = tk.Frame(master=window, bg='#303030')
# s_frame.place(relwidth=1, relheight=1/5)

# s_label = tk.Label(master=s_frame, text="Number of servers (s)", bg=BASE_COL, foreground=TEXT_COL, font=45)
# s_label.place(relx=0, rely=0, relheight=0.15, relwidth=0.25)
# s_entry = tk.Entry(master=s_frame, font=45)
# s_entry.insert(0, "1")
# s_entry.place(relx=0.3, rely=0.05, relheight=0.1, relwidth=0.25)
# s_description = tk.Label(master=s_frame, text="\tThe number of servers denotes how many clients can be dealt with simultaneously.\nAugmenting servers can affect cost.", 
# foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=50)
# s_description.place(relx=0, rely=0.3)

# #Lambda
# l_frame = tk.Frame(master=window, bg='#303030')
# l_frame.place(relwidth=1, relheight=1/5, rely=1/5)

# l_label = tk.Label(master=l_frame, text="Frequence of service" + u" \u03bb", bg=BASE_COL, foreground=TEXT_COL, font=45)
# l_label.place(relx=0, rely=0, relheight=0.15, relwidth=0.25)
# l_entry = tk.Entry(master=l_frame, font=45)
# l_entry.insert(0, u"\u03bb")
# l_entry.place(relx=0.3, rely=0.05, relheight=0.1, relwidth=0.25)
# l_description = tk.Label(master=l_frame, text="\tThe number of servers denotes how many clients can be dealt with simultaneously.\nAugmenting servers can affect cost.", 
# foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=50)
# l_description.place(relx=0, rely=0.3)

# ##Miu
# m_frame = tk.Frame(master=window, bg='#303030')
# m_frame.place(relwidth=1, relheight=1/5, rely=2/5)

# m_label = tk.Label(master=m_frame, text="Service frequence"+ u" \u03bc", bg=BASE_COL, foreground=TEXT_COL, font=45)
# m_label.place(relx=0, rely=0, relheight=0.15, relwidth=0.25)
# m_entry = tk.Entry(master=m_frame, font=45)
# m_entry.insert(0,u"\u03bc")
# m_entry.place(relx=0.3, rely=0.05, relheight=0.1, relwidth=0.25)
# m_description = tk.Label(master=m_frame, text="\tThe number of servers denotes how many clients can be dealt with simultaneously.\nAugmenting servers can affect cost.", 
# foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=50)
# m_description.place(relx=0, rely=0.3)

# ##Expoected customers k
# k_frame = tk.Frame(master=window, bg='#303030')
# k_frame.place(relwidth=1, relheight=1/5, rely=3/5)

# k_label = tk.Label(master=k_frame, text="Number of expected customers", bg=BASE_COL, foreground=TEXT_COL, font=45)
# k_label.place(relx=0, rely=0, relheight=0.15, relwidth=0.3)
# k_entry = tk.Entry(master=k_frame, font=45)
# k_entry.insert(0, "k")
# k_entry.place(relx=0.3, rely=0.05, relheight=0.1, relwidth=0.25)
# k_description = tk.Label(master=k_frame, text="\tk allows to know how many customers to expect into the system.\nIf not applicable, leave as is (k) or blank", 
# foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=50)
# k_description.place(relx=0, rely=0.3)

# ##Std deviation
# sigma_frame = tk.Frame(master=window, bg='#303030')
# sigma_frame.place(relwidth=1, relheight=1/5, rely=4/5)

# sigma_label = tk.Label(master=sigma_frame, text="Standard Deviation (if applicable)" + u" \u03c3", bg=BASE_COL, foreground=TEXT_COL, font=45)
# sigma_label.place(relx=0, rely=0, relheight=0.15, relwidth=0.3)
# sigma_entry = tk.Entry(master=sigma_frame, font=45)
# sigma_entry.insert(0, u"\u03c3")
# sigma_entry.place(relx=0.3, rely=0.05, relheight=0.1, relwidth=0.25)
# sigma_description = tk.Label(master=sigma_frame, text="\tIf a standard deviation is provided, the model M/G/1 will be called.\n If not applicable, leave as is"+ u" (\u03c3)" +" or blank.", 
# foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=50)
# sigma_description.place(relx=0, rely=0.3)

# ok_btn = tk.Button(master=sigma_frame, text="OK", anchor="c", command=lambda: get_results([s_entry.get(), l_entry.get(), m_entry.get(), k_entry.get()]))
# ok_btn.place(relx=0.40, rely=0.7, relheight=0.1, relwidth=0.2)
window.mainloop()