import customtkinter as ctk


class Rectangle(ctk.CTkFrame):
    def __init__(
        self,
        master,
        width=120,
        height=60,
        corner_radius=12,
        text="",
        font=("Arial", 14),
        text_color="black",
        image=None,
        fg_color="#F1F5F9",
        **kwargs
    ):
        super().__init__(
            master,
            width=width,
            height=height,
            corner_radius=corner_radius,
            fg_color=fg_color,
            **kwargs
        )

        # Prevent resizing based on content
        self.pack_propagate(False)
        self.grid_propagate(False)

        self.image = image

        # Center label (text + optional image)
        self.label = ctk.CTkLabel(
            self,
            text=text,
            font=font,
            text_color=text_color,
            image=self.image,
            compound="left" if image else None,  # image + text layout
        )

        self.label.place(relx=0.5, rely=0.5, anchor="center")

    def set_text(self, text):
        self.label.configure(text=text)
