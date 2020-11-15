"""
This module creates the tabs necessary for the queue simulator window.
Called from simulaciondefilas.py
"""

import tkinter as tk
from tkinter import ttk
from tkinter import Entry, messagebox
from enum import Enum
import M_M_s as mms
import mmsk
import M_D_1 as md1
import M_Ek_1 as mek1
import M_G_1 as mg1

HEIGHT = 1300
WIDTH = 1000

# base vals
BASE_COL = "#303030"
TEXT_COL = "#dcdcdc"
FONT_SIZE = 45

# description text
server_description = "\tThe number of servers denotes how many clients can be dealt with simultaneously.\nAugmenting servers can affect cost."
lambda_description = "\tLambda denotes how many clients arrive at the system in a given time interval."
miu_description = "\tMiu denotes the efficiency of a single server.\ni.e. How many clients can be satisfied by a server in a given time interval."
server_cost_description = "\tCost of maintaining a single server over a time interval. (Can be left blank)"
wait_cost_description = "\tCost of keeping a single customer waiting in line. (can be left blank)"
n_pn_description = "\tn will provide Pn, or the probability that there will be n customers in the system. (defaults to 0)"
given_t_decription = "\tt provides the probability that the customer will be waiting more than t units of time in the system"
sigma_entry_description = "\tSigma"+u" \u03c3" + \
    " Denotes the standard deviation of the distribution related to the arrival of customers."
k_entry_description = "\tk is used in a M/M/s/k system to represent how many customers can be expected in a long time period.\nif k is indefinite, use M/M/s"


class Model(Enum):
    MD1 = 1
    MEK1 = 2
    MG1 = 3
    MMS = 4
    MMSK = 5

def invalid_value_error(val):
    messagebox.showerror("Error", "Invalid value for " + val)

def get_results(model, input_dict):
    """
    Receives the input dictionary from the gui form
    specifically, the keys are:
    servers - nonexistent for M/D/1 and M/Ek/1
    lambda - lambda
    miu - miu
    n - prints out Pn, the probability of having n customers in the system
    k - expected customers (only applicable in M/M/s/k)
    sigma - std deviation (only applicable in M/D/1 and M/G/1)
    erlang - k erlang degree (M/Ek/1 only)
    """
    try:
        error_raised = False
        if int(input_dict['lambda'])>=1:
            la = int(input_dict['lambda'])
        else:
            invalid_value_error(u"\u03bb")
            error_raised = True
        if int(input_dict['miu'])>=1:
            mi = int(input_dict['miu'])
        else:
            invalid_value_error(u"\u03bc")
            error_raised = True
        if model not in (Model.MG1, Model.MD1, Model.MEK1):
            if int(input_dict['server_num'])>=1:
                se = int(input_dict['server_num'])
            else:
                error_raised = True
                invalid_value_error("The number of servers")

        if input_dict['n'] == "n" or input_dict['n'] == "":
            n = 0
            messagebox.showinfo("Default value for n", "n will default to 0")
        else:
            if int(input_dict['n'])>=0:
                n = int(input_dict['n'])
            else:
                invalid_value_error("n")
                error_raised = True

        if input_dict['cs'] != "" and input_dict['cw'] != "":
            if int(input_dict['cs'])<0 or int(input_dict['cw'])<0:
                invalid_value_error("Cs or Cw")
                error_raised = True
            else:
                cs = int(input_dict['cs'])
                cw = int(input_dict['cw'])

        else:
            cs, cw = 0, 0
            messagebox.showinfo("No Cs or Cw detected", "Cs and Cw will be equal to 0")

        if model == Model.MMS:
            if int(input_dict['t'])>=0:
                t = float(input_dict['t'])
            else:
                invalid_value_error("t")
                error_raised = True
        elif model == Model.MMSK:
            if int(input_dict['k'])>=0:
                k = int(input_dict['k'])
            else:
                invalid_value_error("k")
                error_raised = True
        elif model == Model.MG1:
            if float(input_dict['sigma'])>=0:
                si = float(input_dict['sigma'])
            else:
                invalid_value_error(u"\u03c3")
                error_raised = True
        elif model == Model.MEK1:
            if int(input_dict['erlang'])>=1:
                er = int(input_dict['erlang'])
            else:
                invalid_value_error("k (Erlang)")
                error_raised = True
    except ValueError as verr:
        error_raised = True
        messagebox.showerror("Error", verr)

    if model == Model.MMS and not error_raised:
        res = mms.mms(la, mi, se, Cs=cs, Cw=cw, t=t, n=n)
    elif model == Model.MMSK and not error_raised:
        res = mmsk.get_mmsk(la, mi, se, k, cw=cw, cs=cs, n=n)
    elif model == Model.MG1 and not error_raised:
        res = mg1.get_m_g_1(la, mi, si, Cs=cs, Cw=cw, n=n)
    elif model == Model.MD1 and not error_raised:
        res = md1.get_m_d_1(la, mi, Cs=cs, Cw=cw, n=n)
    elif model == Model.MEK1 and not error_raised:
        res = mek1.get_m_ek_1(la, mi, er, Cs=cs, Cw=cw, n=n)
    if not error_raised:
        if isinstance(res, dict):
            build_report_win(res)
        else:
            messagebox.showwarning("Warning", "Unstable system i.e. you bit more than you can chew.\nHint: Check lambda, miu and number of servers.")



def build_report_win(res):
    """
    Function to build result window
    res - Dictionary
    """
    res_win = tk.Tk()
    res_win.title("Results")
    canvas = tk.Canvas(res_win, height=HEIGHT, width=WIDTH*0.75)
    canvas.pack()
    resframe = tk.Frame(master=res_win, bg=BASE_COL)
    resframe.place(relheight=1, relwidth=1)
    num_res = len(res)
    i = 0

    for key, value in res.items():
        tk.Label(master=resframe, text=key, font=FONT_SIZE+5, bg=BASE_COL, foreground=TEXT_COL).place(
            relwidth=0.15, relheight=1/num_res, rely=i/num_res)
        tk.Label(master=resframe, text=str(value), font=FONT_SIZE, bg=BASE_COL, foreground=TEXT_COL).place(
            relwidth=0.45, relheight=1/num_res, relx=0.15, rely=i/num_res)
        i += 1


def make_mms_tab(parent_tab, num_components):
    all_rel_height = 1/num_components
    this_frame = 1
    mms_tab = ttk.Frame(master=parent_tab, style='TFrame')
    # The number of servers
    s_frame = ttk.Frame(master=mms_tab)
    s_frame.place(relwidth=1, relheight=all_rel_height)

    s_label = ttk.Label(master=s_frame, text="Number of servers (s)",
                        font=FONT_SIZE, background=BASE_COL, foreground=TEXT_COL)
    s_label.place(relx=0, rely=0, relheight=0.20, relwidth=0.25)
    s_entry = tk.Entry(master=s_frame, font=FONT_SIZE)
    s_entry.insert(0, "1")
    s_entry.place(relx=0.3, rely=0.05, relheight=0.20, relwidth=0.25)
    s_description = tk.Label(master=s_frame, text=server_description,
                             fg=TEXT_COL, bg=BASE_COL, anchor="w", font=FONT_SIZE)
    s_description.place(relx=0, rely=0.3)

    # Lambda
    l_frame = ttk.Frame(master=mms_tab)
    l_frame.place(relwidth=1, relheight=all_rel_height,
                  rely=this_frame/num_components)

    l_label = ttk.Label(master=l_frame, text="Frequence of arrivals" +
                        u" \u03bb", font=FONT_SIZE, background=BASE_COL, foreground=TEXT_COL)
    l_label.place(relx=0, rely=0, relheight=0.20, relwidth=0.25)
    l_entry = tk.Entry(master=l_frame, font=FONT_SIZE)
    l_entry.insert(0, u"\u03bb")
    l_entry.place(relx=0.3, rely=0.05, relheight=0.20, relwidth=0.25)
    l_description = tk.Label(master=l_frame, text=lambda_description,
                             foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=FONT_SIZE)
    l_description.place(relx=0, rely=0.3)
    this_frame += 1

    # Miu
    m_frame = ttk.Frame(master=mms_tab)
    m_frame.place(relwidth=1, relheight=all_rel_height,
                  rely=this_frame/num_components)

    m_label = ttk.Label(master=m_frame, text="Service frequence" +
                        u" \u03bc", font=FONT_SIZE, background=BASE_COL, foreground=TEXT_COL)
    m_label.place(relx=0, rely=0, relheight=0.20, relwidth=0.25)
    m_entry = tk.Entry(master=m_frame, font=FONT_SIZE)
    m_entry.insert(0, u"\u03bc")
    m_entry.place(relx=0.3, rely=0.05, relheight=0.20, relwidth=0.25)
    m_description = tk.Label(master=m_frame, text=miu_description,
                             foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=FONT_SIZE)
    m_description.place(relx=0, rely=0.3)
    this_frame += 1

    # n probability
    n_frame = ttk.Frame(master=mms_tab)
    n_frame.place(relwidth=1, relheight=all_rel_height,
                  rely=this_frame/num_components)

    n_label = ttk.Label(master=n_frame, text="Given n",
                        font=FONT_SIZE, background=BASE_COL, foreground=TEXT_COL)
    n_label.place(relx=0, rely=0, relheight=0.20, relwidth=0.25)
    n_entry = tk.Entry(master=n_frame, font=FONT_SIZE)
    n_entry.insert(0, "n")
    n_entry.place(relx=0.3, rely=0.05, relheight=0.20, relwidth=0.25)
    n_description = tk.Label(master=n_frame, text=n_pn_description,
                             foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=FONT_SIZE)
    n_description.place(relx=0, rely=0.3)
    this_frame += 1

    # time t
    t_frame = ttk.Frame(master=mms_tab)
    t_frame.place(relwidth=1, relheight=all_rel_height,
                  rely=this_frame/num_components)

    t_label = ttk.Label(master=t_frame, text="Given t",
                        font=FONT_SIZE, background=BASE_COL, foreground=TEXT_COL)
    t_label.place(relx=0, rely=0, relheight=0.20, relwidth=0.25)
    t_entry = tk.Entry(master=t_frame, font=FONT_SIZE)
    t_entry.insert(0, "t")
    t_entry.place(relx=0.3, rely=0.05, relheight=0.20, relwidth=0.25)
    t_description = tk.Label(master=t_frame, text=given_t_decription,
                             foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=FONT_SIZE)
    t_description.place(relx=0, rely=0.3)
    this_frame += 1

    # Server cost Cs
    Cs_frame = ttk.Frame(master=mms_tab)
    Cs_frame.place(relwidth=1, relheight=all_rel_height,
                   rely=this_frame/num_components)

    Cs_label = tk.Label(master=Cs_frame, text="Server cost C\u209b",
                        bg=BASE_COL, foreground=TEXT_COL, font=FONT_SIZE)
    Cs_label.place(relx=0, rely=0, relheight=0.20, relwidth=0.3)
    Cs_entry = tk.Entry(master=Cs_frame, font=FONT_SIZE)
    Cs_entry.place(relx=0.3, rely=0.05, relheight=0.20, relwidth=0.25)
    Cs_description = tk.Label(master=Cs_frame, text=server_cost_description,
                              foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=FONT_SIZE)
    Cs_description.place(relx=0, rely=0.3)
    this_frame += 1

    # Cost of waiting in line
    Cw_frame = ttk.Frame(master=mms_tab)
    Cw_frame.place(relwidth=1, relheight=all_rel_height,
                   rely=this_frame/num_components)

    Cw_label = tk.Label(master=Cw_frame, text="Waiting customer in line cos Cw",
                        bg=BASE_COL, foreground=TEXT_COL, font=FONT_SIZE)
    Cw_label.place(relx=0, rely=0, relheight=0.20, relwidth=0.3)
    Cw_entry = tk.Entry(master=Cw_frame, font=FONT_SIZE)
    Cw_entry.place(relx=0.3, rely=0.05, relheight=0.20, relwidth=0.25)
    Cw_description = tk.Label(master=Cw_frame, text=wait_cost_description,
                              foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=FONT_SIZE)
    Cw_description.place(relx=0, rely=0.3)
    this_frame += 1

    # which args to call
    ok_btn = tk.Button(master=Cw_frame, text="OK", anchor="c", command=lambda: get_results(
        Model.MMS, {'server_num':s_entry.get(), 'lambda':l_entry.get(), 'miu':m_entry.get(), 'n':n_entry.get(), 't':t_entry.get(), 'cs':Cs_entry.get(), 'cw':Cw_entry.get()}))
    ok_btn.place(relx=0.40, rely=0.65, relheight=0.15, relwidth=0.2)

    parent_tab.add(mms_tab, text="M/M/s")


def make_mmsk_tab(parent_tab, num_components):
    all_rel_height = 1/num_components
    this_frame = 1
    mmsk_tab = ttk.Frame(master=parent_tab, style='TFrame')
    # The number of servers
    s_frame = ttk.Frame(master=mmsk_tab)
    s_frame.place(relwidth=1, relheight=all_rel_height)

    s_label = ttk.Label(master=s_frame, text="Number of servers (s)",
                        font=FONT_SIZE, background=BASE_COL, foreground=TEXT_COL)
    s_label.place(relx=0, rely=0, relheight=0.20, relwidth=0.25)
    s_entry = tk.Entry(master=s_frame, font=FONT_SIZE)
    s_entry.insert(0, "1")
    s_entry.place(relx=0.3, rely=0.05, relheight=0.20, relwidth=0.25)
    s_description = tk.Label(master=s_frame, text=server_cost_description,
                             fg=TEXT_COL, bg=BASE_COL, anchor="w", font=FONT_SIZE)
    s_description.place(relx=0, rely=0.3)

    # Lambda
    l_frame = ttk.Frame(master=mmsk_tab)
    l_frame.place(relwidth=1, relheight=all_rel_height,
                  rely=this_frame/num_components)

    l_label = ttk.Label(master=l_frame, text="Frequence of service" +
                        u" \u03bb", font=FONT_SIZE, background=BASE_COL, foreground=TEXT_COL)
    l_label.place(relx=0, rely=0, relheight=0.20, relwidth=0.25)
    l_entry = tk.Entry(master=l_frame, font=FONT_SIZE)
    l_entry.insert(0, u"\u03bb")
    l_entry.place(relx=0.3, rely=0.05, relheight=0.20, relwidth=0.25)
    l_description = tk.Label(master=l_frame, text=lambda_description,
                             foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=FONT_SIZE)
    l_description.place(relx=0, rely=0.3)
    this_frame += 1

    # Miu
    m_frame = ttk.Frame(master=mmsk_tab)
    m_frame.place(relwidth=1, relheight=all_rel_height,
                  rely=this_frame/num_components)

    m_label = ttk.Label(master=m_frame, text="Service frequence" +
                        u" \u03bc", font=FONT_SIZE, background=BASE_COL, foreground=TEXT_COL)
    m_label.place(relx=0, rely=0, relheight=0.20, relwidth=0.25)
    m_entry = tk.Entry(master=m_frame, font=FONT_SIZE)
    m_entry.insert(0, u"\u03bc")
    m_entry.place(relx=0.3, rely=0.05, relheight=0.20, relwidth=0.25)
    m_description = tk.Label(master=m_frame, text=miu_description,
                             foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=FONT_SIZE)
    m_description.place(relx=0, rely=0.3)
    this_frame += 1

    # n probability
    n_frame = ttk.Frame(master=mmsk_tab)
    n_frame.place(relwidth=1, relheight=all_rel_height,
                  rely=this_frame/num_components)

    n_label = ttk.Label(master=n_frame, text="Given n",
                        font=FONT_SIZE, background=BASE_COL, foreground=TEXT_COL)
    n_label.place(relx=0, rely=0, relheight=0.20, relwidth=0.25)
    n_entry = tk.Entry(master=n_frame, font=FONT_SIZE)
    n_entry.insert(0, "n")
    n_entry.place(relx=0.3, rely=0.05, relheight=0.20, relwidth=0.25)
    n_description = tk.Label(master=n_frame, text=n_pn_description,
                             foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=FONT_SIZE)
    n_description.place(relx=0, rely=0.3)
    this_frame += 1

    # Cs
    Cs_frame = ttk.Frame(master=mmsk_tab)
    Cs_frame.place(relwidth=1, relheight=all_rel_height,
                   rely=this_frame/num_components)

    Cs_label = ttk.Label(master=Cs_frame, text="Server cost C\u209b",
                         font=FONT_SIZE, background=BASE_COL, foreground=TEXT_COL)
    Cs_label.place(relx=0, rely=0, relheight=0.20, relwidth=0.25)
    Cs_entry = tk.Entry(master=Cs_frame, font=FONT_SIZE)
    Cs_entry.insert(0, u"\u03bc")
    Cs_entry.place(relx=0.3, rely=0.05, relheight=0.20, relwidth=0.25)
    Cs_description = tk.Label(master=Cs_frame, text=server_cost_description,
                              foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=FONT_SIZE)
    Cs_description.place(relx=0, rely=0.3)
    this_frame += 1

    # Cw
    Cw_frame = ttk.Frame(master=mmsk_tab)
    Cw_frame.place(relwidth=1, relheight=all_rel_height,
                   rely=this_frame/num_components)

    Cw_label = ttk.Label(master=Cw_frame, text="Cw",
                         font=FONT_SIZE, background=BASE_COL, foreground=TEXT_COL)
    Cw_label.place(relx=0, rely=0, relheight=0.20, relwidth=0.25)
    Cw_entry = tk.Entry(master=Cw_frame, font=FONT_SIZE)
    Cw_entry.insert(0, u"\u03bc")
    Cw_entry.place(relx=0.3, rely=0.05, relheight=0.20, relwidth=0.25)
    Cw_description = tk.Label(master=Cw_frame, text=wait_cost_description,
                              foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=FONT_SIZE)
    Cw_description.place(relx=0, rely=0.3)
    this_frame += 1

    # Expoected customers k
    k_frame = ttk.Frame(master=mmsk_tab)
    k_frame.place(relwidth=1, relheight=all_rel_height,
                  rely=this_frame/num_components)

    k_label = tk.Label(master=k_frame, text="Number of expected customers",
                       bg=BASE_COL, foreground=TEXT_COL, font=FONT_SIZE)
    k_label.place(relx=0, rely=0, relheight=0.20, relwidth=0.3)
    k_entry = tk.Entry(master=k_frame, font=FONT_SIZE)
    k_entry.insert(0, "k")
    k_entry.place(relx=0.3, rely=0.05, relheight=0.20, relwidth=0.25)
    k_description = tk.Label(master=k_frame, text=k_entry_description,
                             foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=FONT_SIZE)
    k_description.place(relx=0, rely=0.3)
    this_frame += 1

    ok_btn = tk.Button(master=k_frame, text="OK", anchor="c", command=lambda: get_results(Model.MMSK, {'server_num':s_entry.get(), 'lambda':l_entry.get(), 'miu':m_entry.get(), 'n':n_entry.get(), 'cs':Cs_entry.get(), 'cw':Cw_entry.get(), 'k':k_entry.get()}))
    ok_btn.place(relx=0.40, rely=0.65, relheight=0.15, relwidth=0.2)

    parent_tab.add(mmsk_tab, text="M/M/s/k")


def make_mg1_tab(parent_tab, num_components):
    all_rel_height = 1/num_components
    this_frame = 1
    mg1_tab = ttk.Frame(master=parent_tab, style='TFrame')
    # Std deviation
    sigma_frame = ttk.Frame(master=mg1_tab)
    sigma_frame.place(relwidth=1, relheight=all_rel_height)

    sigma_label = ttk.Label(master=sigma_frame, text="Sigma" +
                            u" \u03c3", font=FONT_SIZE, background=BASE_COL, foreground=TEXT_COL)
    sigma_label.place(relx=0, rely=0, relheight=0.20, relwidth=0.25)
    sigma_entry = tk.Entry(master=sigma_frame, font=FONT_SIZE)
    sigma_entry.insert(0, "1")
    sigma_entry.place(relx=0.3, rely=0.05, relheight=0.20, relwidth=0.25)
    sigma_description = tk.Label(master=sigma_frame, text=sigma_entry_description,
                                 fg=TEXT_COL, bg=BASE_COL, anchor="w", font=FONT_SIZE)
    sigma_description.place(relx=0, rely=0.3)

    # Lambda
    l_frame = ttk.Frame(master=mg1_tab)
    l_frame.place(relwidth=1, relheight=all_rel_height,
                  rely=this_frame/num_components)

    l_label = ttk.Label(master=l_frame, text="Frequence of service" +
                        u" \u03bb", font=FONT_SIZE, background=BASE_COL, foreground=TEXT_COL)
    l_label.place(relx=0, rely=0, relheight=0.20, relwidth=0.25)
    l_entry = tk.Entry(master=l_frame, font=FONT_SIZE)
    l_entry.insert(0, u"\u03bb")
    l_entry.place(relx=0.3, rely=0.05, relheight=0.20, relwidth=0.25)
    l_description = tk.Label(master=l_frame, text=lambda_description,
                             foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=FONT_SIZE)
    l_description.place(relx=0, rely=0.3)
    this_frame += 1

    # Miu
    m_frame = ttk.Frame(master=mg1_tab)
    m_frame.place(relwidth=1, relheight=all_rel_height,
                  rely=this_frame/num_components)

    m_label = ttk.Label(master=m_frame, text="Service frequence" +
                        u" \u03bc", font=FONT_SIZE, background=BASE_COL, foreground=TEXT_COL)
    m_label.place(relx=0, rely=0, relheight=0.20, relwidth=0.25)
    m_entry = tk.Entry(master=m_frame, font=FONT_SIZE)
    m_entry.insert(0, u"\u03bc")
    m_entry.place(relx=0.3, rely=0.05, relheight=0.20, relwidth=0.25)
    m_description = tk.Label(master=m_frame, text=miu_description,
                             foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=FONT_SIZE)
    m_description.place(relx=0, rely=0.3)
    this_frame += 1

    # Given n 
    n_frame = ttk.Frame(master=mg1_tab)
    n_frame.place(relwidth=1, relheight=all_rel_height,
                  rely=this_frame/num_components)

    n_label = ttk.Label(master=n_frame, text="Given n",
                        font=FONT_SIZE, background=BASE_COL, foreground=TEXT_COL)
    n_label.place(relx=0, rely=0, relheight=0.20, relwidth=0.25)
    n_entry = tk.Entry(master=n_frame, font=FONT_SIZE)
    n_entry.insert(0, "n")
    n_entry.place(relx=0.3, rely=0.05, relheight=0.20, relwidth=0.25)
    n_description = tk.Label(master=n_frame, text=n_pn_description,
                             foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=FONT_SIZE)
    n_description.place(relx=0, rely=0.3)
    this_frame += 1

    # Expoected customers k
    Cs_frame = ttk.Frame(master=mg1_tab)
    Cs_frame.place(relwidth=1, relheight=all_rel_height,
                   rely=this_frame/num_components)

    Cs_label = tk.Label(master=Cs_frame, text="Server cost C\u209b",
                        bg=BASE_COL, foreground=TEXT_COL, font=FONT_SIZE)
    Cs_label.place(relx=0, rely=0, relheight=0.20, relwidth=0.3)
    Cs_entry = tk.Entry(master=Cs_frame, font=FONT_SIZE)
    Cs_entry.place(relx=0.3, rely=0.05, relheight=0.20, relwidth=0.25)
    Cs_description = tk.Label(master=Cs_frame, text=server_cost_description,
                              foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=FONT_SIZE)
    Cs_description.place(relx=0, rely=0.3)
    this_frame += 1

    # Cost of waiting in line
    Cw_frame = ttk.Frame(master=mg1_tab)
    Cw_frame.place(relwidth=1, relheight=all_rel_height,
                   rely=this_frame/num_components)

    Cw_label = tk.Label(master=Cw_frame, text="Waiting customer in line cos Cw",
                        bg=BASE_COL, foreground=TEXT_COL, font=FONT_SIZE)
    Cw_label.place(relx=0, rely=0, relheight=0.20, relwidth=0.3)
    Cw_entry = tk.Entry(master=Cw_frame, font=FONT_SIZE)
    Cw_entry.place(relx=0.3, rely=0.05, relheight=0.20, relwidth=0.25)
    Cw_description = tk.Label(master=Cw_frame, text=wait_cost_description,
                              foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=FONT_SIZE)
    Cw_description.place(relx=0, rely=0.3)
    this_frame += 1

    ok_btn = tk.Button(master=Cw_frame, text="OK", anchor="c", command=lambda: get_results(
        Model.MG1, {'sigma':sigma_entry.get(), 'lambda':l_entry.get(), 'miu':m_entry.get(), 'n':n_entry.get(), 'cs':Cs_entry.get(), 'cw':Cw_entry.get()}))

    ok_btn.place(relx=0.40, rely=0.65, relheight=0.15, relwidth=0.2)

    parent_tab.add(mg1_tab, text="M/G/1")


def make_md1_tab(parent_tab, num_components):
    all_rel_height = 1/num_components
    this_frame = 1
    md1_tab = ttk.Frame(master=parent_tab, style='TFrame')

    # Lambda
    l_frame = ttk.Frame(master=md1_tab)
    l_frame.place(relwidth=1, relheight=all_rel_height)

    l_label = ttk.Label(master=l_frame, text="Frequence of service" +
                        u" \u03bb", font=FONT_SIZE, background=BASE_COL, foreground=TEXT_COL)
    l_label.place(relx=0, rely=0, relheight=0.20, relwidth=0.25)
    l_entry = tk.Entry(master=l_frame, font=FONT_SIZE)
    l_entry.insert(0, u"\u03bb")
    l_entry.place(relx=0.3, rely=0.05, relheight=0.20, relwidth=0.25)
    l_description = tk.Label(master=l_frame, text=lambda_description,
                             foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=FONT_SIZE)
    l_description.place(relx=0, rely=0.3)

    # Miu
    m_frame = ttk.Frame(master=md1_tab)
    m_frame.place(relwidth=1, relheight=all_rel_height,
                  rely=this_frame/num_components)

    m_label = ttk.Label(master=m_frame, text="Service frequence" +
                        u" \u03bc", font=FONT_SIZE, background=BASE_COL, foreground=TEXT_COL)
    m_label.place(relx=0, rely=0, relheight=0.20, relwidth=0.25)
    m_entry = tk.Entry(master=m_frame, font=FONT_SIZE)
    m_entry.insert(0, u"\u03bc")
    m_entry.place(relx=0.3, rely=0.05, relheight=0.2, relwidth=0.25)
    m_description = tk.Label(master=m_frame, text=miu_description,
                             foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=FONT_SIZE)
    m_description.place(relx=0, rely=0.3)
    this_frame += 1

    # Given n
    n_frame = ttk.Frame(master=md1_tab)
    n_frame.place(relwidth=1, relheight=all_rel_height,
                  rely=this_frame/num_components)

    n_label = ttk.Label(master=n_frame, text="Given n",
                        font=FONT_SIZE, background=BASE_COL, foreground=TEXT_COL)
    n_label.place(relx=0, rely=0, relheight=0.20, relwidth=0.25)
    n_entry = tk.Entry(master=n_frame, font=FONT_SIZE)
    n_entry.insert(0, "n")
    n_entry.place(relx=0.3, rely=0.05, relheight=0.2, relwidth=0.25)
    n_description = tk.Label(master=n_frame, text=n_pn_description,
                             foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=FONT_SIZE)
    n_description.place(relx=0, rely=0.3)
    this_frame += 1

    # Server cost Cs
    Cs_frame = ttk.Frame(master=md1_tab)
    Cs_frame.place(relwidth=1, relheight=all_rel_height,
                   rely=this_frame/num_components)

    Cs_label = tk.Label(master=Cs_frame, text="Server cost C\u209b",
                        bg=BASE_COL, foreground=TEXT_COL, font=FONT_SIZE)
    Cs_label.place(relx=0, rely=0, relheight=0.2, relwidth=0.3)
    Cs_entry = tk.Entry(master=Cs_frame, font=FONT_SIZE)
    Cs_entry.place(relx=0.3, rely=0.05, relheight=0.2, relwidth=0.25)
    Cs_description = tk.Label(master=Cs_frame, text=server_cost_description,
                              foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=FONT_SIZE)
    Cs_description.place(relx=0, rely=0.3)
    this_frame += 1

    # Cost of waiting in line
    Cw_frame = ttk.Frame(master=md1_tab)
    Cw_frame.place(relwidth=1, relheight=all_rel_height,
                   rely=this_frame/num_components)

    Cw_label = tk.Label(master=Cw_frame, text="Waiting customer in line cos Cw",
                        bg=BASE_COL, foreground=TEXT_COL, font=FONT_SIZE)
    Cw_label.place(relx=0, rely=0, relheight=0.2, relwidth=0.3)
    Cw_entry = tk.Entry(master=Cw_frame, font=FONT_SIZE)
    Cw_entry.place(relx=0.3, rely=0.05, relheight=0.2, relwidth=0.25)
    Cw_description = tk.Label(master=Cw_frame, text=wait_cost_description,
                              foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=FONT_SIZE)
    Cw_description.place(relx=0, rely=0.3)
    this_frame += 1

    ok_btn = tk.Button(master=Cw_frame, text="OK", anchor="c", command=lambda: get_results(
        Model.MD1, {'lambda':l_entry.get(), 'miu':m_entry.get(), 'n':n_entry.get(), 'cs':Cs_entry.get(), 'cw':Cw_entry.get()}))

    ok_btn.place(relx=0.40, rely=0.65, relheight=0.2, relwidth=0.2)
    parent_tab.add(md1_tab, text="M/D/1")


def make_mek1_tab(parent_tab, num_components):
    all_rel_height = 1/num_components
    this_frame = 1
    mek1_tab = ttk.Frame(master=parent_tab, style='TFrame')

    # Lambda
    l_frame = ttk.Frame(master=mek1_tab)
    l_frame.place(relwidth=1, relheight=all_rel_height)

    l_label = ttk.Label(master=l_frame, text="Frequence of service" +
                        u" \u03bb", font=FONT_SIZE, background=BASE_COL, foreground=TEXT_COL)
    l_label.place(relx=0, rely=0, relheight=0.20, relwidth=0.25)
    l_entry = tk.Entry(master=l_frame, font=FONT_SIZE)
    l_entry.insert(0, u"\u03bb")
    l_entry.place(relx=0.3, rely=0.05, relheight=0.20, relwidth=0.25)
    l_description = tk.Label(master=l_frame, text=lambda_description,
                             foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=FONT_SIZE)
    l_description.place(relx=0, rely=0.3)

    # Miu
    m_frame = ttk.Frame(master=mek1_tab)
    m_frame.place(relwidth=1, relheight=all_rel_height,
                  rely=this_frame/num_components)

    m_label = ttk.Label(master=m_frame, text="Service frequence" +
                        u" \u03bc", font=FONT_SIZE, background=BASE_COL, foreground=TEXT_COL)
    m_label.place(relx=0, rely=0, relheight=0.20, relwidth=0.25)
    m_entry = tk.Entry(master=m_frame, font=FONT_SIZE)
    m_entry.insert(0, u"\u03bc")
    m_entry.place(relx=0.3, rely=0.05, relheight=0.20, relwidth=0.25)
    m_description = tk.Label(master=m_frame, text=miu_description,
                             foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=FONT_SIZE)
    m_description.place(relx=0, rely=0.3)
    this_frame += 1

    # n
    n_frame = ttk.Frame(master=mek1_tab)
    n_frame.place(relwidth=1, relheight=all_rel_height,
                  rely=this_frame/num_components)

    n_label = ttk.Label(master=n_frame, text="n customers",
                        font=FONT_SIZE, background=BASE_COL, foreground=TEXT_COL)
    n_label.place(relx=0, rely=0, relheight=0.20, relwidth=0.25)
    n_entry = tk.Entry(master=n_frame, font=FONT_SIZE)
    n_entry.insert(0, "n")
    n_entry.place(relx=0.3, rely=0.05, relheight=0.20, relwidth=0.25)
    n_description = tk.Label(master=n_frame, text=n_pn_description,
                             foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=FONT_SIZE)
    n_description.place(relx=0, rely=0.3)
    this_frame += 1

    # Erlang degree k
    k_frame = ttk.Frame(master=mek1_tab)
    k_frame.place(relwidth=1, relheight=all_rel_height,
                  rely=this_frame/num_components)

    k_label = ttk.Label(master=k_frame, text="Erlang degree",
                        font=FONT_SIZE, background=BASE_COL, foreground=TEXT_COL)
    k_label.place(relx=0, rely=0, relheight=0.20, relwidth=0.25)
    k_entry = tk.Entry(master=k_frame, font=FONT_SIZE)
    k_entry.insert(0, "k")
    k_entry.place(relx=0.3, rely=0.05, relheight=0.20, relwidth=0.25)
    k_description = tk.Label(master=k_frame, text=k_entry_description,
                             foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=FONT_SIZE)
    k_description.place(relx=0, rely=0.3)
    this_frame += 1

    # Expoected customers k
    Cs_frame = ttk.Frame(master=mek1_tab)
    Cs_frame.place(relwidth=1, relheight=all_rel_height,
                   rely=this_frame/num_components)

    Cs_label = tk.Label(master=Cs_frame, text="Server cost C\u209b",
                        bg=BASE_COL, foreground=TEXT_COL, font=FONT_SIZE)
    Cs_label.place(relx=0, rely=0, relheight=0.20, relwidth=0.3)
    Cs_entry = tk.Entry(master=Cs_frame, font=FONT_SIZE)
    Cs_entry.place(relx=0.3, rely=0.05, relheight=0.20, relwidth=0.25)
    Cs_description = tk.Label(master=Cs_frame, text=server_cost_description,
                              foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=FONT_SIZE)
    Cs_description.place(relx=0, rely=0.3)
    this_frame += 1

    # Cost of waiting in line
    Cw_frame = ttk.Frame(master=mek1_tab)
    Cw_frame.place(relwidth=1, relheight=all_rel_height,
                   rely=this_frame/num_components)

    Cw_label = tk.Label(master=Cw_frame, text="Waiting customer in line cos Cw",
                        bg=BASE_COL, foreground=TEXT_COL, font=FONT_SIZE)
    Cw_label.place(relx=0, rely=0, relheight=0.20, relwidth=0.3)
    Cw_entry = tk.Entry(master=Cw_frame, font=FONT_SIZE)
    Cw_entry.place(relx=0.3, rely=0.05, relheight=0.20, relwidth=0.25)
    Cw_description = tk.Label(master=Cw_frame, text=wait_cost_description,
                              foreground=TEXT_COL, bg=BASE_COL, anchor="w", font=FONT_SIZE)
    Cw_description.place(relx=0, rely=0.3)
    this_frame += 1

    ok_btn = tk.Button(master=Cw_frame, text="OK", anchor="c", command=lambda: get_results(
        Model.MEK1, {'lambda':l_entry.get(), 'miu':m_entry.get(), 'n':n_entry.get(),'erlang':k_entry, 'cs':Cs_entry.get(), 'cw':Cw_entry.get()}))

    ok_btn.place(relx=0.40, rely=0.65, relheight=0.15, relwidth=0.2)
    parent_tab.add(mek1_tab, text="M/Ek/1")
