import tkinter as tk
from tkinter import ttk
from tkinter import Entry, messagebox
from enum import Enum

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
    s - servers (or sigma) - nonexistent for M/D/1 and M/Ek/1
    l - lambda
    m - miu
    k - (optional) expected customers
    sigma - (optional) std deviation
    """
    try:
        if model != Model.MD1 or model != Model.MEK1:
            s = int(input_list[0])
            l = int(input_list[1])
            m = int(input_list[2])
        else:
            l = int(input_list[0])
            m = int(input_list[1])
    except ValueError as verr:
        messagebox.showerror("Error", verr)
    else:
        res = {}
        if model == Model.MMS:
            n = 1 #TODO unhardcode this
            res = mms.mms(l, m, n, s)
        elif model == Model.MMSK:
            k = int(input_list[3])
            res = mmsk.get_mmsk(l, m, s, k)
        elif model == Model.MG1:
            n = 1 #TODO unhardcode
            res = mg1.get_m_g_1(l, m, n, s, int(input_list[3]), int(input_list[4]))
        elif model == Model.MD1:
            n=1
            res = md1.get_m_d_1(l, m, n, int(input_list[2], int(input_list[3])))
        elif model == Model.MEK1:
            n=1
            k = int(input_list[2])
            res = mek1.get_m_ek_1(l, m, n, k,int(input_list[3], int(input_list[4])))

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
    
def make_mms_tab(parent_tab):
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

    l_label = ttk.Label(master=l_frame, text="Frequence of arrivals" + u" \u03bb", font=45, background=BASE_COL, foreground=TEXT_COL)
    l_label.place(relx=0, rely=0, relheight=0.15, relwidth=0.25)
    l_entry = tk.Entry(master=l_frame, font=45)
    l_entry.insert(0, u"\u03bb")
    l_entry.place(relx=0.3, rely=0.05, relheight=0.1, relwidth=0.25)
    l_description = tk.Label(master=l_frame, text="\tLambda denotes how many clients arrive at the system in a given time interval.", 
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
    m_description = tk.Label(master=m_frame, text="\tMiu denotes the efficiency of a single server.\ni.e. How many clients can be satisfied by a server in a given time interval.", 
    foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=50)
    m_description.place(relx=0, rely=0.3)

    ok_btn = tk.Button(master=m_frame, text="OK", anchor="c", command=lambda: get_results(Model.MMS, [s_entry.get(), l_entry.get(), m_entry.get()]))
    ok_btn.place(relx=0.40, rely=0.7, relheight=0.1, relwidth=0.2)

    parent_tab.add(mms_tab, text="M/M/s")

def make_mmsk_tab(parent_tab):
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
    l_description = tk.Label(master=l_frame, text="\tLambda denotes how many clients arrive at the system in a given time interval.", 
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
    m_description = tk.Label(master=m_frame, text="\tMiu denotes the efficiency of a single server.\ni.e. How many clients can be satisfied by a server in a given time interval.", 
    foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=50)
    m_description.place(relx=0, rely=0.3)

    ##Expoected customers k
    k_frame = ttk.Frame(master=mmsk_tab)
    k_frame.place(relwidth=1, relheight=1/4, rely=3/4)

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

def make_mg1_tab(parent_tab):
    mg1_tab = ttk.Frame(master=parent_tab, style='TFrame')
    ##Std deviation
    sigma_frame = ttk.Frame(master=mg1_tab)
    sigma_frame.place(relwidth=1, relheight=1/5)

    sigma_label = ttk.Label(master=sigma_frame, text="Sigma"+u" \u03c3", font=45, background=BASE_COL, foreground=TEXT_COL)
    sigma_label.place(relx=0, rely=0, relheight=0.15, relwidth=0.25)
    sigma_entry = tk.Entry(master=sigma_frame, font=45)
    sigma_entry.insert(0, "1")
    sigma_entry.place(relx=0.3, rely=0.05, relheight=0.1, relwidth=0.25)
    sigma_description = tk.Label(master=sigma_frame, text="\tSigma"+u" \u03c3"+" Denotes the standard deviation of the distribution related to the arrival of customers.", 
    fg=TEXT_COL, bg=BASE_COL, anchor="w", font=50)
    sigma_description.place(relx=0, rely=0.3)

    #Lambda
    l_frame = ttk.Frame(master=mg1_tab)
    l_frame.place(relwidth=1, relheight=1/5, rely=1/5)

    l_label = ttk.Label(master=l_frame, text="Frequence of service" + u" \u03bb", font=45, background=BASE_COL, foreground=TEXT_COL)
    l_label.place(relx=0, rely=0, relheight=0.15, relwidth=0.25)
    l_entry = tk.Entry(master=l_frame, font=45)
    l_entry.insert(0, u"\u03bb")
    l_entry.place(relx=0.3, rely=0.05, relheight=0.1, relwidth=0.25)
    l_description = tk.Label(master=l_frame, text="\tLambda denotes the efficiency of a single server in a time interval.\ni.e. How many customers can it satisfy in said time interval.", 
    foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=50)
    l_description.place(relx=0, rely=0.3)

    ##Miu
    m_frame = ttk.Frame(master=mg1_tab)
    m_frame.place(relwidth=1, relheight=1/5, rely=2/5)

    m_label = ttk.Label(master=m_frame, text="Service frequence"+ u" \u03bc", font=45, background=BASE_COL, foreground=TEXT_COL)
    m_label.place(relx=0, rely=0, relheight=0.15, relwidth=0.25)
    m_entry = tk.Entry(master=m_frame, font=45)
    m_entry.insert(0,u"\u03bc")
    m_entry.place(relx=0.3, rely=0.05, relheight=0.1, relwidth=0.25)
    m_description = tk.Label(master=m_frame, text="\tThe number of servers denotes how many clients can be dealt with simultaneously.\nAugmenting servers can affect cost.", 
    foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=50)
    m_description.place(relx=0, rely=0.3)

    ##Expoected customers k
    Cs_frame = ttk.Frame(master=mg1_tab)
    Cs_frame.place(relwidth=1, relheight=1/5, rely=3/5)

    Cs_label = tk.Label(master=Cs_frame, text="Server cost C\u209b", bg=BASE_COL, foreground=TEXT_COL, font=45)
    Cs_label.place(relx=0, rely=0, relheight=0.15, relwidth=0.3)
    Cs_entry = tk.Entry(master=Cs_frame, font=45)
    Cs_entry.place(relx=0.3, rely=0.05, relheight=0.1, relwidth=0.25)
    Cs_description = tk.Label(master=Cs_frame, text="\tCost of maintaining a single server over a time interval. (Can be left blank)", 
    foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=50)
    Cs_description.place(relx=0, rely=0.3)

    ##Cost of waiting in line
    Cw_frame = ttk.Frame(master=mg1_tab)
    Cw_frame.place(relwidth=1, relheight=1/5, rely=4/5)

    Cw_label = tk.Label(master=Cw_frame, text="Waiting customer in line cos Cw", bg=BASE_COL, foreground=TEXT_COL, font=45)
    Cw_label.place(relx=0, rely=0, relheight=0.15, relwidth=0.3)
    Cw_entry = tk.Entry(master=Cw_frame, font=45)
    Cw_entry.place(relx=0.3, rely=0.05, relheight=0.1, relwidth=0.25)
    Cw_description = tk.Label(master=Cw_frame, text="\tCost of keeping a single customer waiting in line. (can be left blank)", 
    foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=50)
    Cw_description.place(relx=0, rely=0.3)

    if Cs_entry.get() == "" or Cw_entry.get() == "":
        ok_btn = tk.Button(master=Cw_frame, text="OK", anchor="c", command=lambda: get_results(Model.MG1, [sigma_entry.get(), l_entry.get(), m_entry.get(), Cs_entry.get(), Cw_entry.get()]))
        ok_btn.place(relx=0.40, rely=0.65, relheight=0.1, relwidth=0.2)
    else:
        ok_btn = tk.Button(master=Cw_frame, text="OK", anchor="c", command=lambda: get_results(Model.MG1, [sigma_entry.get(), l_entry.get(), m_entry.get()]))
        ok_btn.place(relx=0.40, rely=0.65, relheight=0.1, relwidth=0.2)

    parent_tab.add(mg1_tab, text="M/G/1")

def make_md1_tab(parent_tab):
    md1_tab = ttk.Frame(master=parent_tab, style='TFrame')

    ##Std deviation
    sigma_frame = ttk.Frame(master=md1_tab)
    sigma_frame.place(relwidth=1, relheight=1/5)

    sigma_label = ttk.Label(master=sigma_frame, text="Sigma"+u" \u03c3", font=45, background=BASE_COL, foreground=TEXT_COL)
    sigma_label.place(relx=0, rely=0, relheight=0.15, relwidth=0.25)
    sigma_entry = tk.Entry(master=sigma_frame, font=45)
    sigma_entry.insert(0, "1")
    sigma_entry.place(relx=0.3, rely=0.05, relheight=0.1, relwidth=0.25)
    sigma_description = tk.Label(master=sigma_frame, text="\tSigma"+u" \u03c3"+" Denotes the standard deviation of the distribution related to the arrival of customers.", 
    fg=TEXT_COL, bg=BASE_COL, anchor="w", font=50)
    sigma_description.place(relx=0, rely=0.3)

    #Lambda
    l_frame = ttk.Frame(master=md1_tab)
    l_frame.place(relwidth=1, relheight=1/5, rely=1/5)

    l_label = ttk.Label(master=l_frame, text="Frequence of service" + u" \u03bb", font=45, background=BASE_COL, foreground=TEXT_COL)
    l_label.place(relx=0, rely=0, relheight=0.15, relwidth=0.25)
    l_entry = tk.Entry(master=l_frame, font=45)
    l_entry.insert(0, u"\u03bb")
    l_entry.place(relx=0.3, rely=0.05, relheight=0.1, relwidth=0.25)
    l_description = tk.Label(master=l_frame, text="\tLambda denotes the efficiency of a single server in a time interval.\ni.e. How many customers can it satisfy in said time interval.", 
    foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=50)
    l_description.place(relx=0, rely=0.3)

    ##Miu
    m_frame = ttk.Frame(master=md1_tab)
    m_frame.place(relwidth=1, relheight=1/5, rely=2/5)

    m_label = ttk.Label(master=m_frame, text="Service frequence"+ u" \u03bc", font=45, background=BASE_COL, foreground=TEXT_COL)
    m_label.place(relx=0, rely=0, relheight=0.15, relwidth=0.25)
    m_entry = tk.Entry(master=m_frame, font=45)
    m_entry.insert(0,u"\u03bc")
    m_entry.place(relx=0.3, rely=0.05, relheight=0.1, relwidth=0.25)
    m_description = tk.Label(master=m_frame, text="\tThe number of servers denotes how many clients can be dealt with simultaneously.\nAugmenting servers can affect cost.", 
    foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=50)
    m_description.place(relx=0, rely=0.3)

    ##Expoected customers k
    Cs_frame = ttk.Frame(master=md1_tab)
    Cs_frame.place(relwidth=1, relheight=1/5, rely=3/5)

    Cs_label = tk.Label(master=Cs_frame, text="Server cost C\u209b", bg=BASE_COL, foreground=TEXT_COL, font=45)
    Cs_label.place(relx=0, rely=0, relheight=0.15, relwidth=0.3)
    Cs_entry = tk.Entry(master=Cs_frame, font=45)
    Cs_entry.place(relx=0.3, rely=0.05, relheight=0.1, relwidth=0.25)
    Cs_description = tk.Label(master=Cs_frame, text="\tCost of maintaining a single server over a time interval. (Can be left blank)", 
    foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=50)
    Cs_description.place(relx=0, rely=0.3)

    ##Cost of waiting in line
    Cw_frame = ttk.Frame(master=md1_tab)
    Cw_frame.place(relwidth=1, relheight=1/5, rely=4/5)

    Cw_label = tk.Label(master=Cw_frame, text="Waiting customer in line cos Cw", bg=BASE_COL, foreground=TEXT_COL, font=45)
    Cw_label.place(relx=0, rely=0, relheight=0.15, relwidth=0.3)
    Cw_entry = tk.Entry(master=Cw_frame, font=45)
    Cw_entry.place(relx=0.3, rely=0.05, relheight=0.1, relwidth=0.25)
    Cw_description = tk.Label(master=Cw_frame, text="\tCost of keeping a single customer waiting in line. (can be left blank)", 
    foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=50)
    Cw_description.place(relx=0, rely=0.3)

    if Cs_entry.get() == "" and Cw_entry.get() == "":
        ok_btn = tk.Button(master=Cw_frame, text="OK", anchor="c", command=lambda: get_results(Model.MD1, [sigma_entry.get(), l_entry.get(), m_entry.get(), Cs_entry.get(), Cw_entry.get()]))
        ok_btn.place(relx=0.40, rely=0.65, relheight=0.1, relwidth=0.2)
    else:
        ok_btn = tk.Button(master=Cw_frame, text="OK", anchor="c", command=lambda: get_results(Model.MD1, [sigma_entry.get(), l_entry.get(), m_entry.get()]))
        ok_btn.place(relx=0.40, rely=0.65, relheight=0.1, relwidth=0.2)

    parent_tab.add(md1_tab, text="M/D/1")

def make_mek1_tab(parent_tab):
    mek1_tab = ttk.Frame(master=parent_tab, style='TFrame')

    #Lambda
    l_frame = ttk.Frame(master=mek1_tab)
    l_frame.place(relwidth=1, relheight=1/6)

    l_label = ttk.Label(master=l_frame, text="Frequence of service" + u" \u03bb", font=45, background=BASE_COL, foreground=TEXT_COL)
    l_label.place(relx=0, rely=0, relheight=0.15, relwidth=0.25)
    l_entry = tk.Entry(master=l_frame, font=45)
    l_entry.insert(0, u"\u03bb")
    l_entry.place(relx=0.3, rely=0.05, relheight=0.1, relwidth=0.25)
    l_description = tk.Label(master=l_frame, text="\tLambda denotes the efficiency of a single server in a time interval.\ni.e. How many customers can it satisfy in said time interval.", 
    foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=50)
    l_description.place(relx=0, rely=0.3)

    ##Miu
    m_frame = ttk.Frame(master=mek1_tab)
    m_frame.place(relwidth=1, relheight=1/6, rely=1/6)

    m_label = ttk.Label(master=m_frame, text="Service frequence"+ u" \u03bc", font=45, background=BASE_COL, foreground=TEXT_COL)
    m_label.place(relx=0, rely=0, relheight=0.15, relwidth=0.25)
    m_entry = tk.Entry(master=m_frame, font=45)
    m_entry.insert(0,u"\u03bc")
    m_entry.place(relx=0.3, rely=0.05, relheight=0.1, relwidth=0.25)
    m_description = tk.Label(master=m_frame, text="\tThe number of servers denotes how many clients can be dealt with simultaneously.\nAugmenting servers can affect cost.", 
    foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=50)
    m_description.place(relx=0, rely=0.3)

    ##n
    n_frame = ttk.Frame(master=mek1_tab)
    n_frame.place(relwidth=1, relheight=1/6, rely=2/6)

    n_label = ttk.Label(master=n_frame, text="n customers", font=45, background=BASE_COL, foreground=TEXT_COL)
    n_label.place(relx=0, rely=0, relheight=0.15, relwidth=0.25)
    n_entry = tk.Entry(master=n_frame, font=45)
    n_entry.insert(0,"n")
    n_entry.place(relx=0.3, rely=0.05, relheight=0.1, relwidth=0.25)
    n_description = tk.Label(master=n_frame, text="\tThe number of servers denotes how many clients can be dealt with simultaneously.\nAugmenting servers can affect cost.", 
    foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=50)
    n_description.place(relx=0, rely=0.3)

    ## Erlang degree k
    k_frame = ttk.Frame(master=mek1_tab)
    k_frame.place(relwidth=1, relheight=1/6, rely=3/6)

    k_label = ttk.Label(master=k_frame, text="Erlang degree", font=45, background=BASE_COL, foreground=TEXT_COL)
    k_label.place(relx=0, rely=0, relheight=0.15, relwidth=0.25)
    k_entry = tk.Entry(master=k_frame, font=45)
    k_entry.insert(0,"k")
    k_entry.place(relx=0.3, rely=0.05, relheight=0.1, relwidth=0.25)
    k_description = tk.Label(master=k_frame, text="\tThe number of servers denotes how many clients can be dealt with simultaneously.\nAugmenting servers can affect cost.", 
    foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=50)
    k_description.place(relx=0, rely=0.3)

    ##Expoected customers k
    Cs_frame = ttk.Frame(master=mek1_tab)
    Cs_frame.place(relwidth=1, relheight=1/6, rely=4/6)

    Cs_label = tk.Label(master=Cs_frame, text="Server cost C\u209b", bg=BASE_COL, foreground=TEXT_COL, font=45)
    Cs_label.place(relx=0, rely=0, relheight=0.15, relwidth=0.3)
    Cs_entry = tk.Entry(master=Cs_frame, font=45)
    Cs_entry.place(relx=0.3, rely=0.05, relheight=0.1, relwidth=0.25)
    Cs_description = tk.Label(master=Cs_frame, text="\tCost of maintaining a single server over a time interval. (Can be left blank)", 
    foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=50)
    Cs_description.place(relx=0, rely=0.3)

    ##Cost of waiting in line
    Cw_frame = ttk.Frame(master=mek1_tab)
    Cw_frame.place(relwidth=1, relheight=1/6, rely=5/6)

    Cw_label = tk.Label(master=Cw_frame, text="Waiting customer in line cos Cw", bg=BASE_COL, foreground=TEXT_COL, font=45)
    Cw_label.place(relx=0, rely=0, relheight=0.15, relwidth=0.3)
    Cw_entry = tk.Entry(master=Cw_frame, font=45)
    Cw_entry.place(relx=0.3, rely=0.05, relheight=0.1, relwidth=0.25)
    Cw_description = tk.Label(master=Cw_frame, text="\tCost of keeping a single customer waiting in line. (can be left blank)", 
    foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=50)
    Cw_description.place(relx=0, rely=0.3)

    if Cs_entry.get() == "" and Cw_entry.get() == "":
        ok_btn = tk.Button(master=Cw_frame, text="OK", anchor="c", command=lambda: get_results(Model.MEK1, [l_entry, m_entry, n_entry, k_entry, Cs_entry, Cw_entry]))
        ok_btn.place(relx=0.40, rely=0.65, relheight=0.1, relwidth=0.2)
    else:
        ok_btn = tk.Button(master=Cw_frame, text="OK", anchor="c", command=lambda: get_results(Model.MEK1, [l_entry, m_entry, n_entry, k_entry]))
        ok_btn.place(relx=0.40, rely=0.65, relheight=0.1, relwidth=0.2)

    parent_tab.add(mek1_tab, text="M/Ek/1")

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


############################################ M/M/s TAB #######################################################

make_mms_tab(parent_tab)

######################################################  M/M/s/k  TAB   ###########################################################

make_mmsk_tab(parent_tab)

# ################################################ M/G/1 TAB ###################################################

make_mg1_tab(parent_tab)

# ############################################## M/D/1 TAB ####################################################

make_md1_tab(parent_tab)

# ############################################# M/Ek/1 TAB ####################################################

make_mek1_tab(parent_tab)

#adding all tabs to the window
parent_tab.pack(expand=1, fill="both")

window.mainloop()