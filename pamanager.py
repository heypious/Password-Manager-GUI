from random import randint, shuffle, choice
from pymongo import MongoClient
from tkinter import messagebox
# import customtkinter as ct
# from PIL import Image
import json

SERVER = r"mongodb+srv://test:test@mirrorbot.fgzyaml.mongodb.net/?retryWrites=true&w=majority"
DATABASE = "mypass"
COLLECTION = "collection"
JSON = "./data.json"

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
        if email not in json_data[website].keys():
            raise KeyError
    except KeyError:
        messagebox.showerror(title="Error", message="No details for the website exists")
    else:
        password = json_data[website][email]
        messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    random_letters = [choice(letters) for _ in range(randint(8, 10))]
    random_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    random_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = random_numbers + random_symbols + random_letters
    shuffle(password_list)

    password = "".join(password_list)

    pass_input.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = web_input.get()
    email = email_input.get()
    password = pass_input.get()
    if not len(website) or not len(password):
        messagebox.showwarning(title="Oops", message="Please don't leave any fields empty")
    else:
        with open("data.json", "r") as data:
            try:
                json_data = json.load(data)
            except json.decoder.JSONDecodeError:
                json_data = {}
        if website not in json_data:
            json_data[website] = {}
        json_data[website][email] = password
        with open("data.json", "w") as data:
            json.dump(json_data, data, indent=4)
        sync()
        web_input.delete("0", "end")
        pass_input.delete("0", "end")


def sync():
    client = MongoClient(SERVER)
    db = client[DATABASE]
    collection = db[COLLECTION]

    with open(JSON, "r") as localdb:
        data = json.load(localdb)

    # Replace existing documents:
    collection.delete_many({})  # Clear existing data
    collection.insert_one(data)  # Insert the new data
    client.close()

    messagebox.showinfo(title="Success", message="Uploaded JSON data to MongoDB successfully!")



def get():
    client = MongoClient(SERVER)
    db = client[DATABASE]
    collection = db[COLLECTION]

    documents = collection.find()
    mongo = [docs for docs in documents]
    mongo_data = mongo[0]
    del mongo_data['_id']
    try:
        with open(JSON, 'r') as localdb:
            try:
                local_data = json.load(localdb)
            except json.decoder.JSONDecodeError:
                local_data = {}
    except:
        with open(JSON, 'w') as localdb:
            local_data = {}
    # Compare dictionaries based on website keys and email entries:
    has_more_data = False
    for website in mongo_data:
        if website not in local_data or len(mongo_data[website]) > len(local_data.get(website, {})):
            has_more_data = True
            break

    if has_more_data:
        with open(JSON, 'w') as localdb:  # Overwrite existing file
            json.dump(mongo_data, localdb, indent=4)
        messagebox.showinfo(title="Success", message="MongoDB data written to local JSON file!")
    else:
        messagebox.showinfo(title="Info", message="Local JSON file is up-to-date.")

    client.close()



# window = ct.CTk()
# ct.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
# ct.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
# 
# window.title("Password Manager")
# window.config(padx=20, pady=20)
# 
# # Create a frame to organize elements
# frame = ct.CTkFrame(master=window)
# frame.grid(row=0, column=0, sticky="nsew")  # Expand frame to fill window
# # window.grid_rowconfigure(0, weight=1)
# # window.grid_columnconfigure(0, weight=1)  # Allow frame to expand
# 
# logo_image = ct.CTkImage(Image.open("assets/logo.png"), size=(200, 200))
# logo_label = ct.CTkLabel(master=frame, text="", image=logo_image)
# logo_label.grid(column=1, row=0, padx=20, pady=20)  # Place logo within the frame
# 
# sync_image = ct.CTkImage(Image.open("assets/upload.png"), size=(25, 25))
# sync_button = ct.CTkButton(master=frame, image=sync_image, command=sync, text="", height=25, width=25)
# sync_button.grid(column=2, row=0, sticky="ne")
# 
# get_image = ct.CTkImage(Image.open("assets/download.png"), size=(25, 25))
# get_button = ct.CTkButton(master=frame, image=get_image, command=get, text="", height=25, width=25)
# get_button.grid(column=0, row=0, sticky="nw")
# 
# # Labels
# web_label = ct.CTkLabel(master=frame, text="Website:")
# web_label.grid(column=0, row=1, sticky="w")
# web_label.focus()
# 
# email_label = ct.CTkLabel(master=frame, text="Email:")
# email_label.grid(column=0, row=2, sticky="w")
# 
# pass_label = ct.CTkLabel(master=frame, text="Password:")
# pass_label.grid(column=0, row=3, sticky="w")
# 
# # Entries
# web_input = ct.CTkEntry(master=frame, width=26)
# web_input.grid(column=1, row=1, sticky="we", padx=10, pady=5)
# 
# email_input = ct.CTkEntry(master=frame, width=35)
# email_input.grid(column=1, row=2, sticky="we", padx=10, pady=5)
# email_input.insert(0, "foo@email.com")
# 
# pass_input = ct.CTkEntry(master=frame, width=26)
# pass_input.grid(column=1, row=3, sticky="we", padx=10, pady=5)
# 
# # Buttons
# search_button = ct.CTkButton(master=frame, text="Search", command=find_password, width=20)
# search_button.grid(column=2, row=1, sticky="we", padx=5)
# 
# gen_button = ct.CTkButton(master=frame, text="Generate", command=generate_password, width=20)
# gen_button.grid(column=2, row=3, sticky="we", padx=5)
# 
# add_button = ct.CTkButton(master=frame, text="Add", width=36, command=save)
# add_button.grid(column=1, row=4, sticky="we", pady=5)
# 
# window.mainloop()
