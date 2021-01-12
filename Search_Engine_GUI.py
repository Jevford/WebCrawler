
import Search_Engine_Indexer
import Search_Engine_Query_Process 
import tkinter as tk
import webbrowser
import math

Window = tk.Tk()
Window.geometry("1920x1080")
Window.title("Search Engine")

web_page = []
#hyperlink
def open_url(event):
    webbrowser.open_new(event.widget.cget("text"))

def retrieve_input_query():
    global query_content
    query_content = text_box.get("1.0", "end-1c")
    global web_page
    web_page = Search_Engine_Query_Process.search_query(query_content.lower())


'''
def check(len_of_description):
    basic_len = 40
    basic_times = 7
    diff  =abs(len_of_description-basic_len)
    if(len_of_description>basic_len):
        diff_per = diff/100
        basic_times-diff_per
        if(len_of_description>100):
            basic_times-=0.5
    else:
        diff_per = diff/10
        basic_times+=math.ceil(diff_per)
        if(len_of_description<5):
            basic_times+=4
    return len_of_description*basic_times

''' 
def search():
    local_text_x = 15
    local_text_y =110
    retrieve_input_query()
    
    global text_list    
    global label_list

    print('\n')
    print("Your Search Query: " + query_content + '\n')
    rankCount = 1
    for item in web_page:
        print(str(rankCount) + ": " + item[1])
        rankCount += 1
    # for i in range(len(web_page)):
    #     text_list[i]['text']=web_page[i][0]+":"
    #     text_list[i].place(x=local_text_x,y=local_text_y)
        
    #     len_of_description = len(web_page[i][0])
        
    #     label_list[i]['text'] = web_page[i][1][:105]


        #label_list[i].place(x=check(len_of_description),y=local_text_y)
        #local_text_y+=28

    # for i in range(len(web_page),20):
    #     text_list[i]['text']=""
    #     text_list[i].place(x=local_text_x,y=local_text_y)
    #     label_list[i]['text']=""


        #label_list[i].place(x=check(len_of_description),y=local_text_y)
        #local_text_y+=28
    
# Label Managers
#a list of label
label_list = []
for i in range(20):
    current_label= tk.Label(Window,text="12",fg="blue",cursor="hand2")
    current_label.bind("<Button-1>",open_url)
    label_list.append(current_label)

text_list=[]
for i in range(20):
    current_lab = tk.Label(Window,text="")
    text_list.append(current_lab)


# Creating Widgets

# Labels
label_1 = tk.Label(Window, text = " Welcome to Our Search Engine! ",
            bd=2,
            font = ('Arial', 30),
            width=25,
            height=0)
label_1.grid(column=1, row=0)


label_2 = tk.Label(Window, text="Input Query:",
            bd=2,
            font = ('Arial', 18), 
            width = 15)
label_2.grid(column=0, row=1)

text_box = tk.Text(Window, font = ('Arial', 14), bg = 'light green', height = 1.5, width = 80)
text_box.grid(column=0, columnspan=3, row=1, padx=20, pady=0, ipadx=50)

button = tk.Button(Window, height = 0, width = 10, font = ('Arial', 18), text = "Search", command = search)
button.grid(column=2, row=1)

search_result_canvas = tk.Canvas(width=1400, height=700, bg='white')
search_result_canvas.grid(column=0, row=2, columnspan=3, padx=65, pady=5)

Window.mainloop()
