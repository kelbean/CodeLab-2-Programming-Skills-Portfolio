"""

Exercise 03 - Student Manager
By: Kelvin Marron Bautista
CYL5

"""

# NOTE: I decided to use the Treeview widget from ttk because I wanted to present the student records in a tabular form.
# Although I'm quite unfamiliar with the widget, I used online sources for reference to help with my coding.
# Sources can be found within the code (at the Treeview section)

# Importing all the necessary modules

from tkinter import * # Imported all Tkinter functions to create the GUI
from tkinter import ttk # Imported ttk for treeview and styling
from tkinter import messagebox # Imported messagebox for pop-ups
from PIL import Image, ImageTk # Imported PIL (Pillow) to handle images in Tkinter (for aesthetic purposes)
import os # Imported the OS module to deal with file paths just in case directory errors occur

# File path handling (this is to ensure resources within the file environment can be imported safely without error)

script_dir = os.path.dirname(os.path.abspath(__file__)) # This command gets the script's folder
os.chdir(script_dir) # The working directory would then be changed to the script's folder

# Setting up the tkinter window

main = Tk()
main.title("Student Manager") # An appropriate title for the student management system program
main.geometry("1000x500")
main.resizable(0,0) # Disables window resizing
main.config(bg="#171717") # As always, dark theme wins!

# Functions

def load_student_data(filename="studentMarks.txt"): # This opens up the student dataset and organizes everything to put it into the records listing.
    students = [] # This list will store all student data tuples
    try:
        with open(filename, 'r') as f: # Reads the txt file
            lines = f.readlines()[1:]  # Here, the first line was skipped because it gives the number of students in the class
        for line in lines:
            if not line.strip(): # This is to skip any blank lines
                continue

            # Here, each line is split into different fields for their respective data. Since a comma separates each data, it's easier to organize.
            code, name, *marks, exam = line.strip().split(',')
            marks = list(map(int, marks)) # This converts the coursework marks into integers and lists them
            exam = int(exam) # Same goes for exam marks: they are converted into integers as well
            total_score = sum(marks) + exam # Sum of marks and exam marks are calculated
            percentage = (total_score / 160) * 100 # Assuming 160 total marks max (based on the instructions)

            # Grade will be stored based on the percentage:
            grade = (
                'A' if percentage >= 70 else
                'B' if percentage >= 60 else
                'C' if percentage >= 50 else
                'D' if percentage >= 40 else
                'F'
            )

            # Here, the command will append the formatted tuple into the students list:
            students.append((int(code), name, sum(marks), exam, f"{percentage:.2f}", grade)) #

    except FileNotFoundError: # Just in case file wasn't found, a pop-up will come up
        messagebox.showwarning("Warning", f"File '{filename}' not found!")
    return students # List of all processed student data will then be returned

# Managing the treeview (student records list)

def clear_tree(): # This function loops through each current row and deletes them
    for row in tree.get_children():
        tree.delete(row)

def view_records(): # This function displays the processed data into the listing on screen
    clear_tree()
    students = load_student_data()
    for s in students: # Each student record is inserted into the Treeview widget
        tree.insert("", END, values=s)

def show_highest_mark(): # This function displays the student with the highest mark
    clear_tree()
    students = load_student_data()
    if students:
        highest = max(students, key=lambda s: float(s[4])) # Used a lambda here to extract the percentage (located in index 4) and find the max (less space)
        tree.insert("", END, values=highest)

def show_lowest_mark(): # This function displays the student with the lowest mark
    clear_tree()
    students = load_student_data()
    if students:
        lowest = min(students, key=lambda s: float(s[4])) # This finds the student with the lowest %
        tree.insert("", END, values=lowest)

# Selecting an individual student record

def refresh_student_dict(): # I created this function to make sure the combobox is updated with the available names and IDs
    global student_dict
    students = load_student_data()
    # Created a dictionary here mapping "Name (ID)" from the full data tuple (To make it look organized in the combobox)
    student_dict = {f"{s[1]} ({s[0]})": s for s in students}
    combo['values'] = list(student_dict.keys()) # This updates the combobox list

def show_selected_student(event=None): # This function just displays the selected student's data from the dropdown
    selected = student_select.get()
    if not selected:
        messagebox.showwarning("Warning", "Please select a student.") # Pop-up shows up to prevent empty selections
        return
    student_data = student_dict.get(selected)

    
    # This retrieves the tuple (record) for the selected student in the student record listing
    if student_data:
        clear_tree()
        tree.insert("", END, values=student_data)

# UI Layout (Wanted to make it slightly professional representing a database system)

# Main container (contains the left frame and right frame)
container = Frame(main, bg="#171717")
container.pack(side=TOP, fill=BOTH, expand=True, padx=20, pady=20)

# Left Frame (Management buttons are located here)
left_frame = Frame(container, bg="#171717")
left_frame.pack(side=LEFT, fill=Y, padx=15, pady=15)

# Logo (Decided to give the database system a logo because why not?)
logo_image = Image.open("management_logo.png") # 'management_logo.png' is opened
logo_image = logo_image.resize((100, 100)) # Sets the image to 100x100 pixels
logo = ImageTk.PhotoImage(logo_image) # This converts it to a Tkinter-compatible image
logo_label = Label(left_frame, image=logo, bg="#171717") # A label is then created to display the imported image
logo_label.pack(pady=10) # Image is placed. Padding is also adjusted here. More spacing above and less spacing under.

Label(left_frame, text="Management:", bg="#171717", fg="white", font=("Arial", 10)).pack(pady=5) 

# Management buttons
Button(left_frame, text="View all records", width=15, bg="#185e8d", fg="white", command=view_records).pack(pady=5, fill=X) # Calls view_records when pressed
Button(left_frame, text="Show highest mark", width=15, bg="#185e8d", fg="white", command=show_highest_mark).pack(pady=5, fill=X) # Calls show_highest_mark when pressed
Button(left_frame, text="Show lowest mark", width=15, bg="#185e8d", fg="white", command=show_lowest_mark).pack(pady=5, fill=X) # Calls show_lowest_mark when pressed

# Individual student dropdown
Label(left_frame, text="View individual student:", bg="#171717", fg="white", font=("Arial", 10)).pack(pady=(15,5))
student_select = StringVar() # This variable holds the selected combobox value
combo = ttk.Combobox(left_frame, textvariable=student_select, state="readonly")
combo.pack(fill=X, pady=5)
combo.bind("<<ComboboxSelected>>", show_selected_student) # When the user selects a student, the student's record is shown on the listing

# Right Frame (This contains the Treeview itself which is meant to list the student records)
right_frame = Frame(container, bg="#171717")
right_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=5, pady=5)

# I was quite unfamiliar with Treeview so I used an online source for reference to organize the student data
# Reference: Treeview, URL: https://tkdocs.com/tutorial/tree.html

# Treeview structure
columns = ("code", "name", "coursework", "exam", "percent", "grade") # Columns are defined here

tree = ttk.Treeview(right_frame, columns=columns, show="headings") # Treeview widget then shows the tabular data
tree.pack(fill=BOTH, expand=True)

# Column configuration
tree.column("code", width=60, anchor=CENTER)
tree.column("name", width=150, anchor=W)
tree.column("coursework", width=90, anchor=CENTER)
tree.column("exam", width=80, anchor=CENTER)
tree.column("percent", width=90, anchor=CENTER)
tree.column("grade", width=60, anchor=CENTER) 

# Defining column headers
tree.heading("code", text="ID")
tree.heading("name", text="Name")
tree.heading("coursework", text="Coursework")
tree.heading("exam", text="Exam")
tree.heading("percent", text="Percentage")
tree.heading("grade", text="Grade")

# Styling the treeview (ttk takes a different approach in styling so I used an online source for reference)
# Reference: ttk widget, https://docs.python.org/3/library/tkinter.ttk.html
# 
style = ttk.Style()
style.theme_use("default")  # allows custom colors

# Customizing the row colors
style.configure("Treeview", background="#1e1e1e", foreground="white", rowheight=25, fieldbackground="#1e1e1e", bordercolor="#2b2b2b", borderwidth=1)

# Customizing the headers
style.configure("Treeview.Heading", background="#333333", foreground="white", padding=5, font=('Segoe UI', 10), relief="flat")

# Hover header selection color
style.map("Treeview.Heading", background=[("active", "#555555")])

# Customizing for when a record is selected
style.map("Treeview", background=[("selected", "#0078D7")], foreground=[("selected", "white")])

# Initializing the data
student_dict = {}
refresh_student_dict() # This populates the dropdown on startup

# Run
main.mainloop()