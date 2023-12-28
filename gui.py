
import customtkinter as ct
from PIL import Image
from pmanager import *
window = ct.CTk()
ct.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ct.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

window.title("Password Manager")
window.config(padx=20, pady=20)
window.grid_rowconfigure(0, weight=1)
# window.grid_columnconfigure(0, weight=1)

# frame = ct.CTkFrame(master=window)
# frame.pack(padx=20, pady=20, )
# frame.place(anchor='center', relx=0.5, rely=0.5)

logo_image = ct.CTkImage(Image.open("assets/logo.png"), size=(200, 200))
logo_label = ct.CTkLabel(master=window, text="", image=logo_image)
logo_label.grid(column=1, row=0)

sync_image = ct.CTkImage(Image.open("assets/upload.png"), size=(25, 25))
sync_button = ct.CTkButton(master=window, image=sync_image, command=sync, text="", height=25, width=25)
sync_button.grid(column=2, row=0, sticky="n")

get_image = ct.CTkImage(Image.open("assets/download.png"), size=(25, 25))
get_button = ct.CTkButton(master=window, image=get_image, command=get, text="", height=25, width=25)
get_button.grid(column=0, row=0, sticky="n")

# Labels
web_label = ct.CTkLabel(master=window, text="Website:")
web_label.grid(column=0, row=1, sticky="w")
web_label.focus()

email_label = ct.CTkLabel(master=window, text="Email:")
email_label.grid(column=0, row=2, sticky="w")

pass_label = ct.CTkLabel(master=window, text="Password:")
pass_label.grid(column=0, row=3, sticky="w")

# Entries
web_input = ct.CTkEntry(master=window, width=26)
web_input.grid(column=1, row=1, sticky="we", padx=10, pady=5)

email_input = ct.CTkEntry(master=window, width=35)
email_input.grid(column=1, row=2, sticky="we", padx=10, pady=5)
email_input.insert(0, "foo@email.com")

pass_input = ct.CTkEntry(master=window, width=26)
pass_input.grid(column=1, row=3, sticky="we", padx=10, pady=5)

# Buttons
search_button = ct.CTkButton(master=window, text="Search", command=find_password, width=20)
search_button.grid(column=2, row=1, sticky="we", padx=5)

gen_button = ct.CTkButton(master=window, text="Generate", command=generate_password, width=20)
gen_button.grid(column=2, row=3, sticky="we", padx=5)

add_button = ct.CTkButton(master=window, text="Add", width=36, command=save)
add_button.grid(column=1, row=4, sticky="we", pady=5)

window.mainloop()
