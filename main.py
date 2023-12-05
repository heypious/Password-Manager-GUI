import tkinter as tk
from tkinter import messagebox
from random import randint, shuffle, choice
import pyperclip
import json

# ---------------------------- SEARCH  ------------------------------- #


def find_password():
    website = web_input.get()
    email = email_input.get()

    try:
        with open("data.json", "r") as data:
            json_data = json.load(data)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File Found.")
    try:
        if not email in json_data[website].keys():
            raise KeyError
    except KeyError:
        messagebox.showerror(title="Error", message="No details for the website exists")
    else:
        password = json_data[website][email]
        messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    random_letters = [choice(letters) for _ in range(randint(8, 10))]
    random_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    random_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = random_numbers + random_symbols + random_letters
    shuffle(password_list)

    password = "".join(password_list)

    pass_input.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = web_input.get()
    email = email_input.get()
    password = pass_input.get()
    new_data = {
        website: {
            email : password,
        }
    }

    if not len(website) or not len(password):
        messagebox.showwarning(title="Oops", message="Please don't leave any fields empty")

    else:
        try:
            with open("data.json", "r") as data:
                json_data = json.load(data)
        except FileNotFoundError:
            with open("data.json", "w") as data:
                json.dump(new_data, data, indent=4)
        else:
            json_data[website][email] = password 
            with open("data.json", "w") as data:
                json.dump(json_data, data, indent=4)
        finally:
            web_input.delete("0", "end")
            pass_input.delete("0", "end")


# ---------------------------- UI SETUP ------------------------------- #

window = tk.Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = tk.Canvas(width=200, height=200)
logo = tk.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=1, column=2)

# Labels
web_label = tk.Label(text="Website:")
web_label.grid(row=2, column=1)
web_label.focus()

email_label = tk.Label(text="Email/Username:")
email_label.grid(row=3, column=1)

pass_label = tk.Label(text="Password:")
pass_label.grid(row=4, column=1)

# Entries
web_input = tk.Entry(width=26)
web_input.grid(row=2, column=2, columnspan=1)

email_input = tk.Entry(width=35)
email_input.grid(row=3, column=2, columnspan=2)
email_input.insert(0, "foo@email.com")

pass_input = tk.Entry(width=26)
pass_input.grid(row=4, column=2, columnspan=1)

# Buttons
search_button = tk.Button(text="    Search    ", command=find_password)
search_button.grid(row=2, column=3, columnspan=2)

gen_button = tk.Button(text="Generate Password", command=generate_password)
gen_button.grid(row=4, column=3, columnspan=2)

add_button = tk.Button(text="Add", width=36, command=save)
add_button.grid(row=5, column=2, columnspan=2)


window.mainloop()


