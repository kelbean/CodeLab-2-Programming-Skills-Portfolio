"""

Exercise 01 - Maths Quiz
By: Kelvin Marron Bautista
CYL5

"""

# Importing all the necessary modules

from tkinter import * # Imported all Tkinter functions to create the GUI
from tkinter import messagebox # Imported messagebox to send alert pop-ups for errors
import random # Imported random to generate random numbers for the math quiz questions
from PIL import Image, ImageTk # Imported PIL (Pillow) to handle images in Tkinter (for aesthetic purposes)
import os # Imported the OS module to deal with file paths just in case directory errors come up

# File path handling (this is to ensure resources within the file environment can be imported safely without error)

script_dir = os.path.dirname(os.path.abspath(__file__)) # This command gets the script's folder
os.chdir(script_dir) # The working directory would then be changed to the script's folder

# Setting up the tkinter window

root = Tk() # Created an object 'root' to handle the main Tkinter window
root.title("Math Mania") # Sets the window title (I thought 'Math Mania' would be a cool name)
root.geometry("700x450") # Sets the window size
root.resizable(0,0) # Disables window resizing
root.config(bg="#171717") # Always been a fan of dark themed applications because it's so easy on the eyes!

# Functions

def displayMenu(): # This function displays the menu (where the user selects a difficulty level)
    menu_frame.pack(pady=50)
    quiz_frame.pack_forget() # Quiz frame is hidden
    result_frame.pack_forget() # Results frame is hidden

def randomInt(level): # This function is basically the randomizer. It'll return integers based on the difficulty level selected.
    if level == 1:  # Easy: 1 digit
        return random.randint(1, 9), random.randint(1, 9)
    elif level == 2:  # Moderate: 2 digits
        return random.randint(10, 99), random.randint(10, 99)
    else:  # Advanced: up to 4 digits
        return random.randint(1000, 9999), random.randint(1000, 9999)

def decideOperation(): # This function will decide which operation to use (addition or subtraction)
    return random.choice(['+', '-']) # Random will choose between the two

def displayProblem(): # This function displays the math problem on screen for the user
    global first_attempt
    first_attempt = True # User's first attempt is marked
    a, b = randomInt(difficulty_level) # Randomizer sets the integers for a, b based on the difficulty level
    operation = decideOperation() # The decideOperation function sets the operation sign (+ or -)
    problem_frame.problem = (a, b, operation) # Stores the problem data in the frame
    problem_label.config(text=f"{a} {operation} {b}") # Updates the text and sets it as the random math problem created
    answer_entry.delete(0, END) # Clears any previous input inside the entry

def isCorrect(): # This function serves as a correction detector. It also records the score of the user.
    global score, question_count, first_attempt
    a, b, operation = problem_frame.problem # This will retrieve the current problem for checking

    # Input checking

    try:
        user_ans = int(answer_entry.get()) # Input from the entry box will be converted to integer
    except ValueError:
        messagebox.showwarning("Invalid", "Please enter a number.") # If not an integer, warning pop-up will show up.
        return
    
    # Checking if the answer is correct
    
    correct_ans = a + b if operation == '+' else a - b # Simple arithmetic operators are used here to calculate the right answer
    
    if user_ans == correct_ans:
        points_gained = 10 if first_attempt else 5 # First attempt rewards 10 points and second attempt rewards 5
        score += points_gained # Points are added
        question_count += 1
        if question_count < 10: # If question is still not finished, math problems will keep displaying on screen
            displayProblem()
        else:
            displayResults() # Once finished, results will be shown
    else: # Wrong answer would execute the following:
        if first_attempt:
            first_attempt = False # First attempt will be marked false
            messagebox.showinfo("Try Again", "Incorrect! You have one more attempt.") # Pop-up to warn the user of one more attempt to answer
        else: # This marks the second attempt
            question_count += 1
            if question_count < 10:
                displayProblem()
            else:
                displayResults() # This will show the results after the last question

def displayResults(): # This displays the user's score and rank throughout the math quiz
    quiz_frame.pack_forget() # Quiz frame is hidden after the quiz is done
    result_frame.pack(pady=50) # Results frame comes in
    rank = ""
    

    # Depending on the user's score, a rank will be given:
    if score > 90:
        rank = "A+"
    elif score > 80:
        rank = "A"
    elif score > 70:
        rank = "B"
    elif score > 60:
        rank = "C"
    elif score > 50:
        rank = "D"
    else:
        rank = "F"
    result_label.config(text=f"Score: {score}/100\nRank: {rank}") # Results are updated with the user's score and rank

def startQuiz(level): # This function is to start the quiz entirely
    global difficulty_level, score, question_count
    difficulty_level = level
    score = 0
    question_count = 0
    menu_frame.pack_forget() # Hide the menu frame once quiz starts
    result_frame.pack_forget() # Hide results frame and save it for last
    quiz_frame.pack(pady=50) # Show quiz frame to display the math problems
    displayProblem() # Problem display function is called

def playAgain(): # Returns to the main menu if the user wishes to play again
    displayMenu()

# Menu frame (The startup main menu where the user selects a difficulty level)
menu_frame = Frame(root, bg="#171717")

# Math quiz logo (for aesthetic purposes)

logo_image = Image.open("maths_quiz_logo.png") # 'maths_quiz_logo.png' is opened
logo_image = logo_image.resize((100, 100)) # Sets the image to 100x100 pixels
logo = ImageTk.PhotoImage(logo_image) # This converts it to a Tkinter-compatible image
logo_label = Label(menu_frame, image=logo, bg="#171717") # A label is then created to display the imported image
logo_label.pack(pady=10) # Image is placed and padding is adjusted.

# Menu widgets

Label(menu_frame, text="Welcome to Math Mania!", font=("Verdana", 20, "bold"), bg="#171717", fg="white").pack(pady=(0,5))
Label(menu_frame, text="Pick a difficulty level to start:", font=("Verdana", 16), bg="#171717", fg="white").pack(pady=(0,10))

# For the buttons, 'command' expects a function to call when the button is clicked.
# We use 'lambda' to pass an argument to that function since the startQuiz function requires the number to set the quiz difficulty

Button(menu_frame, text="Easy", width=20, command=lambda: startQuiz(1), bg="#3C995B", fg="white").pack(pady=5)
Button(menu_frame, text="Moderate", width=20, command=lambda: startQuiz(2), bg="#9BA12D", fg="white").pack(pady=5)
Button(menu_frame, text="Advanced", width=20, command=lambda: startQuiz(3), bg="#9E2626", fg="white").pack(pady=5)

# Quiz frame

quiz_frame = Frame(root, bg="#171717") # The quiz frame itself to display the problem and entry widget
quiz_frame.pack(expand=True)
problem_frame = Frame(quiz_frame, bg="#171717")
problem_frame.pack(pady=(60, 0))
problem_label = Label(problem_frame, text="", font=("Arial", 35, "bold"), bg="#171717", fg="white") # Will contain the randomized problem
problem_label.pack()
answer_entry = Entry(quiz_frame, width=30) # Entry widget for the user to put in their answers
answer_entry.pack(pady=15)
Button(quiz_frame, text="Submit", command=isCorrect, bg="#1D4770", fg="white").pack(pady=10) # The submission button is backed by isCorrect to check the answer
note_label = Label(quiz_frame, text="Note: You only have 2 attempts per question. Think carefully!", bg="#171717", fg="gray") # Just a note to remind the user of their attempts
note_label.pack(pady=15)

# Results frame (Just a simple frame that shows up at the end of the quiz to display the user's results)

result_frame = Frame(root, bg="#171717")
result_label = Label(result_frame, text="", font=("Arial", 26, "bold"), bg="#171717", fg="white")
result_label.pack(pady=(60,0))
Button(result_frame, text="Play again!", width=25, command=playAgain, bg="#1D4770", fg="white").pack(pady=20) # Play again button activates the playAgain function and returns the user to the main menu
Button(result_frame, text="Quit..", width=25, command=root.quit, bg="#701D1D", fg="white").pack(pady=5) # Quits the program once pressed

# Menu will show up once the program is booted

displayMenu()

# Run

root.mainloop()
