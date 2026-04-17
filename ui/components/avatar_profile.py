import customtkinter as ctk


class AvatarProfile(ctk.CTkFrame):
    def __init__(
        self,
        master,
        width=70,
        height=70,
        text="A",
        text_color="white",
        font=("Arial", 20, "bold"),
        **kwargs
    ):
        super().__init__(
            master,
            width=width,
            height=height,
            corner_radius=min(width, height) // 2,
            **kwargs
        )

        # 🔥 prevent shrinking
        self.pack_propagate(False)
        self.grid_propagate(False)

        # 🔥 label in center
        self.label = ctk.CTkLabel(self, text=text, text_color=text_color, font=font)
        self.label.place(relx=0.5, rely=0.5, anchor="center")

    # 🔥 change text dynamically
    def set_text(self, new_text):
        self.label.configure(text=new_text)

    # 🔥 optional: change text color too
    def set_text_color(self, new_color):
        self.label.configure(text_color=new_color)
