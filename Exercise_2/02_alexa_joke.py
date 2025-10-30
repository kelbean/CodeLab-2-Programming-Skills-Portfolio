"""

Exercise 02 - Alexa, tell me a joke!
By: Kelvin Marron Bautista
CYL5

"""

# Importing all the necessary modules:

from tkinter import * # Imported all Tkinter functions to create the GUI
import random # Imported the random module to select jokes randomly from the provided dataset
from PIL import Image, ImageTk # Imported PIL (Pillow) to handle images in Tkinter (for aesthetic purposes)
import os # Imported the OS module to deal with file paths just in case directory errors occur

# File path handling (this is to ensure resources within the file environment can be imported safely without error)

script_dir = os.path.dirname(os.path.abspath(__file__)) # This command gets the script's folder
os.chdir(script_dir) # The working directory would then be changed to the script's folder

# Setting up the tkinter window

root = Tk() # Created an object 'root' to handle the main Tkinter window
root.title("Alexa the Jokester") # Gave the program a simple title to fit the exercise task (An Alexa program that tells jokes)
root.geometry("580x360") # As a simple joke program, I gave it a fairly smaller size compared to the other exercises.
root.resizable(0,0) # Disables window resizing
root.config(bg="#1A1A1A") # Dark theme

# Loading the jokes dataset (resource: randomJokes.txt)

with open("randomJokes.txt", "r", encoding="utf-8") as f: # Opening the 'randomJokes.txt' file in read mode with UTF-8 encoding ('with' then safely closes the file after reading)
    jokes = [line.strip() for line in f if "?" in line] # Reads each line in the dataset and strips any leading/trailing spaces. It also keeps lines with ?.
jokes = [j.split("?", 1) for j in jokes] # Each line that contains a joke is split into two parts at the first '?'
# The first part (index 0) is the joke setup, the second part (index 1) is the punchline. The command separates the two.

# Initializing these variables to store whether or not the joke or punchline is shown on screen

current_joke = None
punchline_shown = False

# Functions
def process_input(): # This function handles whatever the user types in the entry box. The entry must follow requirements for results to show up.
    global current_joke, punchline_shown
    user_text = user_entry.get().strip().lower() # This gets the user input from the entry box, removes any spaces, and converts to lowercase for easier matching.
    user_entry.delete(0, END) # This clears the entry box after handling the user's input.

    if user_text == "alexa tell me a joke": # If the user types "Alexa tell me a joke", it'll execute the following:
        current_joke = random.choice(jokes) # This picks a random joke from the list
        punchline_shown = False # This resets the punchline state because a new joke has been selected
        main_label.config(text=current_joke[0] + "?") # The '0' index selects the joke itself and a question mark is added at the end. The label config then displays the setup.
        info_label.config(text='Type "?" and press Enter to see the punchline', fg="gray") # This label updates and informs the user what to type to see the punchline

    elif current_joke and not punchline_shown and user_text == "?": # If the current joke is selected and the punchline hasn't been shown yet, and user types ?, the following executes:
        main_label.config(text=current_joke[1].strip()) # The '1' index selects the punchline and displays it. The config updates the text.
        punchline_shown = True
        info_label.config(text='Type "Alexa tell me a joke" for another one!', fg="gray") # Here, joke and punchline have been shown. Info label reminds the user to prompt for another joke if they wish.

    elif current_joke and not punchline_shown: # Current joke is selected and punchline is not shown but the user typed anything other than '?', the following is executed:
        info_label.config(text='Type "?" to reveal the punchline.', fg="gray") # This updates the previous label and reminds the user to type '?' to see the punchline.
    else: # No joke has been selected or the user's input didn't follow the requirements so the following is executed:
        info_label.config(text='Type "Alexa tell me a joke" to get a joke.', fg="gray") # Info label is updated to remind the user how to start the program

# Clown image (for aesthetic purposes)

clown_image = Image.open("clown.png") # 'clown.png' is opened
clown_image = clown_image.resize((100, 100)) # Sets the image to 100x100 pixels
clown = ImageTk.PhotoImage(clown_image) # This converts it to a Tkinter-compatible image
clown_label = Label(root, image=clown, bg="#1A1A1A") # A label is then created to display the imported image
clown_label.pack(pady=(30,5)) # Image is placed. Padding is also adjusted here. More spacing above and less spacing under.

# Main label (I prefer one label because it can just get updated which I find to be more convenient for this kind of program)

main_label = Label(root, text="Hey there, I'm Alexa!\nA professional jokester at your service!", font=("Arial", 16, "bold"), justify="center", bg="#1A1A1A", fg="white", wraplength=500)
main_label.pack(pady=(10,15), padx=15)

# User input
user_entry = Entry(root, width=30, font=("Arial", 12)) # Entry widget is used here for the user's input
user_entry.pack(pady=5)
user_entry.focus() # For user convenience purposes. This makes it so that the user can type in text immediately after running the program.

# Enter button
enter_btn = Button(root, text="Enter", width=15, command=process_input, bg="#A32929", fg="white") # Button widget is used here to activate the function
enter_btn.pack(pady=(10, 10))

# Info label (Added this to guide the user. The text updates itself whenever a requirement is not followed.)
info_label = Label(root, text='Type "Alexa tell me a joke" to get started.', font=("Verdana", 10, "italic"), bg="#1A1A1A", fg="gray")
info_label.pack(pady=(5, 20))

# Run
root.mainloop()
