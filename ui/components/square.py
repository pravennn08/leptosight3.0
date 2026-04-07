import customtkinter as ctk


class Square(ctk.CTkFrame):
    def __init__(
        self,
        master,
        size=60,
        corner_radius=16,
        image=None,
        fg_color="#F1F5F9",
        **kwargs
    ):
        super().__init__(
            master,
            width=size,
            height=size,
            corner_radius=corner_radius,
            fg_color=fg_color,
            **kwargs
        )

        self.pack_propagate(False)
        self.grid_propagate(False)

        self.image = image

        if self.image:
            self.label = ctk.CTkLabel(self, image=self.image, text="")
            self.label.place(relx=0.5, rely=0.5, anchor="center")
