# import customtkinter

# class App(customtkinter.CTk):
#     def __init__(self):
#         super().__init__()

#         self.title("LeptoSight | Sign In")


#         self.button = customtkinter.CTkButton(self, text="my button", command=self.button_callbck)
#         self.button.pack(padx=20, pady=20)


#         self.bind("<Escape>", lambda e: self.destroy())

#     def button_callbck(self):
#         print("button clicked")

# app = App()
# app.attributes('-fullscreen', True)
# app.mainloop()

# import customtkinter
# from constants.seeds import BACKGROUND, PRIMARY, SECONDARY, HOVER

# class App(customtkinter.CTk):
#     def __init__(self):
#         super().__init__(fg_color=BACKGROUND)
#         self.title("LeptoSight | Sign In")


#         self.button = customtkinter.CTkButton(
#             self, text="my button", height=100, width=100, fg_color=PRIMARY, hover_color=SECONDARY,command=self.button_callbck
#         )
#         self.button.pack(padx=20, pady=20)

#         self.bind("<Escape>", lambda e: self.destroy())

#     def button_callbck(self):
#         print("button clicked")

# app = App()
# app.attributes("-zoomed", True)
# # app.attributes('-fullscreen', True)
# app.mainloop()

from ui.app import App

app = App()
app.attributes("-zoomed", True)
app.mainloop()
