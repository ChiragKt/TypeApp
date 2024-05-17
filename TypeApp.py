from tkinter import *
from tkinter import colorchooser, messagebox, filedialog, simpledialog, END
import time

def auto_save():
    global autosave_interval
    text = text_space.get('1.0', END)
    with open("TypeApp-AUTOSAVE.txt", 'w') as file:
        file.write(text)
    window.after(autosave_interval * 1000, auto_save)

def prompt_save():
    save_prompt = messagebox.askyesnocancel(title="WARNING!", message="Do you want to save the current file?")
    if save_prompt is None:
        return False
    elif save_prompt:
        save_file()
    return True

def new_file():
    if text_space.get("1.0", "end-1c") != "":
        if prompt_save():
            text_space.delete('1.0', END)
            messagebox.showinfo(title="Alert", message="New File Created")
    else:
        messagebox.showinfo(title="Alert", message="New File Created")

def open_file():
    if not prompt_save():
        return

    path = filedialog.askopenfilename()
    if path:
        try:
            with open(path, 'r') as file:
                text = file.read()
                text_space.delete('1.0', END)
                text_space.insert('1.0', text)
        except Exception as e:
            messagebox.showerror(message=f"Unable to open file: {e}")
    else:
        messagebox.showinfo(message="No file selected.")

def save_file():
    path = filedialog.asksaveasfilename(defaultextension="txt", filetypes=[("Text File", ".txt"), ("Other", ".*")])
    if path:
        with open(path, 'w') as file:
            text = text_space.get('1.0', END)
            file.write(text)
    else:
        messagebox.showerror(message="File not saved.")

def current_time():
    if clock_state:
        time_string = time.strftime("%I:%M:%S %p")
        clock.config(text=time_string)
        window.after(1000, current_time)

def clock_on_off():
    global clock_state
    if clock_state:
        clock_state = False
        clock.config(text="")
    else:
        clock_state = True
        current_time()

def change_clock_size(size):
    if clock_state:
        if size == "Small":
            clock.config(font=("Arial", 10, "bold"))
        elif size == "Medium":
            clock.config(font=("Arial", 13, "bold"))
        elif size == "Large":
            clock.config(font=("Arial", 16, "bold"))

def about():
    messagebox.showinfo(message="Developed By Chirag Kataria\nVersion: 1.0")

def find_and_replace():
    find_word = simpledialog.askstring("Find & Replace", "Enter the word to Find. (Case-Sensitive)")
    replace_word = simpledialog.askstring("Find & Replace", "Enter the word to Replace. (Case-Sensitive)")

    if find_word and replace_word:
        text = text_space.get("1.0", "end")
        updated_text = text.replace(find_word, replace_word)
        if text == updated_text:
            messagebox.showinfo("No Match", "No occurrences of '{}' found.".format(find_word))
        else:
            text_space.delete("1.0", "end")
            text_space.insert("1.0", updated_text)

def word_count():
    text = text_space.get('1.0', "end-1c")
    text_list = text.split()
    length = len(text_list)
    messagebox.showinfo(title="Word Count", message=f"Words: {length}")

def highlight_selected_text():
    start_index = text_space.index("sel.first")
    end_index = text_space.index("sel.last")
    is_highlighted = "highlight" in text_space.tag_names(start_index)
    if is_highlighted:
        text_space.tag_remove("highlight", start_index, end_index)
    else:
        text_space.tag_add("highlight", start_index, end_index)

def change_background():
    global theme
    new_theme = colorchooser.askcolor()
    if new_theme[1] is not None:
        text_space.config(bg=new_theme[1])
        theme = new_theme[1]

def set_default_background():
    default = "#FFFCC1"
    text_space.config(bg=default)

def change_font(new_font):
    global font
    font = new_font
    text_space.config(font=(font, font_size))

def change_font_size(new_size):
    global font_size
    font_size = new_size
    text_space.config(font=(font, font_size))

def change_font_color():
    new_color = colorchooser.askcolor()
    if new_color[1] is not None:
        text_space.config(fg=new_color[1])

theme = "#FFFCC1"
font_color = "Black"
font = "Arial"
font_size = 25
font_list = [
    'Arial', 'Arial Black', 'Book Antiqua', 'Bookman Old Style', 'Calibri',
    'Cambria', 'Century Gothic', 'Comic Sans MS', 'Courier New', 'Georgia',
    'Helvetica', 'Impact', 'Lucida Console', 'Palatino', 'Tahoma', 'Times New Roman',
    'Trebuchet MS', 'Verdana', 'Symbol', 'Wingdings'
]

clock_size_list = ["Small", "Medium", "Large"]
font_size_list = [10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 35, 37, 40, 45, 47, 49, 50]
clock_state = True
autosave_interval = 60

window = Tk()
window.config(bg=theme)
window.title("TypeApp")
window.geometry("720x720")

app_name = Label(text="TypeApp", fg="#A555EC", bg=theme, font=("Helvetica", 25, "bold"))
app_name.pack(side="top", fill="x")

clock = Label(window, font=("Arial", 12, "bold"), bg=theme, fg="Black")
clock.place(relx=1.0, rely=0, anchor='ne')

text_space = Text(window, bg=theme, fg=font_color, font=(font, font_size), undo=True)
text_space.pack(fill=BOTH, expand=True)

menu_bar = Menu(window)
window.config(menu=menu_bar)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
menu_bar.add_cascade(label="File", menu=file_menu)

edit_menu = Menu(menu_bar, tearoff=0)

font_menu = Menu(edit_menu)
for f in font_list:
    font_menu.add_command(label=str(f), command=lambda f=f: change_font(f))

edit_menu.add_cascade(label="Font", menu=font_menu)

font_size_menu = Menu(edit_menu)
for s in font_size_list:
    font_size_menu.add_command(label=str(s), command=lambda s=s: change_font_size(s))

clock_menu = Menu(menu_bar)
clock_size_menu = Menu(clock_menu)

clock_menu.add_command(label="On/Off", command=clock_on_off)
clock_menu.add_cascade(label="Size", menu=clock_size_menu)

for size in clock_size_list:
    clock_size_menu.add_command(label=size, command=lambda s=size: change_clock_size(s))

background_color_menu = Menu(edit_menu)
background_color_menu.add_command(label="Default", command=set_default_background)
background_color_menu.add_command(label="Choose Color", command=change_background)
edit_menu.add_cascade(label="Font Size", menu=font_size_menu)
edit_menu.add_command(label="Font Color", command=change_font_color)
edit_menu.add_cascade(label="Background Color", menu=background_color_menu)
edit_menu.add_command(label="Highlight Text", command=highlight_selected_text)
text_space.tag_configure("highlight", background="yellow")

text_menu = Menu(menu_bar)
text_menu.add_command(label="Find & Replace", command=find_and_replace)
text_menu.add_command(label="Word Count", command=word_count)
text_menu.add_separator()
text_menu.add_command(label="Undo", command=text_space.edit_undo)
text_menu.add_command(label="Redo", command=text_space.edit_redo)

about_menu = Menu(menu_bar)
about_menu.add_command(label="About", command=about)

menu_bar.add_cascade(label="Text", menu=text_menu)
menu_bar.add_cascade(label="Format", menu=edit_menu)
menu_bar.add_cascade(label="Clock", menu=clock_menu)
menu_bar.add_cascade(label="Help", menu=about_menu)

window.bind("<Control-z>", lambda event: text_space.edit_undo())
window.bind("<Control-Z>", lambda event: text_space.edit_undo())
window.bind("<Control-Shift-Z>", lambda event: text_space.edit_redo())
window.bind("<Control-Shift-z>", lambda event: text_space.edit_redo())
window.bind("<Command-z>", lambda event: text_space.edit_undo())
window.bind("<Command-Z>", lambda event: text_space.edit_undo())
window.bind("<Command-Shift-Z>", lambda event: text_space.edit_redo())
window.bind("<Command-Shift-z>", lambda event: text_space.edit_redo())

auto_save()
window.mainloop()
