from tkinter import *
import Search_Engine_Indexer
import Search_Engine_Query_Process 
import math

Window = Tk()
Window.geometry("1500x1000")
Window.title("Search Engine")

search_result_canvas = Canvas(width = 1400, height = 600, bg = 'white')
search_result_canvas.place(x = 10, y = 150)


label_list = []
for i in range(20):
    current_label= Label(Window,text="12",fg="blue",cursor="hand2")
    label_list.append(current_label)

text_list=[]
for i in range(20):
    empty = Label(Window,text="")
    text_list.append(empty)



# Label
label_1 = Label(Window, text = " Welcome to Our Search Engine! ",
            bd=2,
            font = ('Arial', 30),
            width=25,
            height=2)

label_2 = Label(Window, text = "Search Result: ", 
            font = ('Arial', 18), 
            width = 15, 
            height = 2)



text_box = Text(Window, bg = 'light green', height = 2, width = 95)
web_page = []
def retrieve_input_query():
    query_content = text_box.get("1.0", "end-1c")
    global web_page
    web_page = Search_Engine_Query_Process.search_query(query_content)



def check_len(len_of_description):
    threshold_len = 40
    initial = 7
    diff = abs(len_of_description - threshold_len)
    if len_of_description < threshold_len:
        diff_rate = diff/10
        initial += math.ceil(diff_rate)
        return len_of_description*initial
    else:
        diff_rate = diff/100
        #initial -= diff_rate
        if(len_of_description>100):
            initial -= 0.5
        return len_of_description*(initial+1)



def search():
    description_text_x = 20
    description_text_y = 150
    retrieve_input_query()
    global text_list    
    global label_list

    rankCount = 1
    for item in web_page:
        print(str(rankCount) + ": " + item[1])
        rankCount += 1

    for i in range(len(web_page)):
        text_list[i]['text'] = web_page[i][0] + ": "
        text_list[i].place(x = description_text_x, y = description_text_y)
        
        len_of_description = len(web_page[i][0])
        #print(str(i)+"  "+str(len_of_description))
        label_list[i]['text'] = web_page[i][1][:205]
        label_list[i].place(x = check_len(len_of_description), y = description_text_y)
        description_text_y += 25
    
    for i in range(len(web_page),20):
        try:
            text_list[i]['text']=""
            text_list[i].place(x = description_text_x,y = description_text_y)
            label_list[i]['text']=""
            label_list[i].place(x=check_len(len_of_description),y = description_text_y)
            description_text_y += 25
        except:
            print("No result from the corpus.")
            text_list[i]['text'] = "No result from the corpus."
            text_list[i].place(x = description_text_x,y = description_text_y)
            return 
    


scrollbar = Scrollbar(Window, orient = HORIZONTAL, command = search_result_canvas.xview) 
#scrollbar.set(0.3, 1)
#scrollbar.pack(side = "bottom", fill = "x")
scrollbar.place(x = 450, y = 750, width=180, height=20)
#scrollbar.configure(command = Window.xview)
search_result_canvas.config(xscrollcommand = scrollbar.set)
scrollbar.pack(side = "bottom", fill = "x")



label_1.pack()
label_2.place(x = 0, y = 100)
text_box.place(x = 375, y = 60)

button = Button(Window, height = 2, width = 10, font = ('Arial', 18), text = "Search", command = search)
button.place(x = 1150, y = 60)

Window.mainloop()