from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")

to_learn = data.to_dict(orient="records")
current_card = {}


def new_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_displayed, image=card_front_image)
    flip_timer = window.after(3000, func=flip_card)


def known_word():
    to_learn.remove(current_card)
    known_data = pandas.DataFrame(to_learn)
    known_data.to_csv("data/words_to_learn.csv", index=False)

    new_card()


def flip_card():
    canvas.itemconfig(card_displayed, image=card_back_image)
    canvas.itemconfig(card_title, fill="white", text="English")
    canvas.itemconfig(card_word, fill="white", text=current_card["English"])


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR, highlightthickness=0)
flip_timer = window.after(3000, func=flip_card)

# Card
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
card_displayed = canvas.create_image(400, 263, image=card_front_image)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# Buttons
tick_image = PhotoImage(file="images/right.png")
x_image = PhotoImage(file="images/wrong.png")

tick_button = Button(image=tick_image, highlightthickness=0, command=known_word)
tick_button.grid(column=1, row=1)

x_button = Button(image=x_image, highlightthickness=0, command=new_card)
x_button.grid(column=0, row=1)

new_card()

window.mainloop()
