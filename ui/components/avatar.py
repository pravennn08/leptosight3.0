import customtkinter as ctk


class Avatar(ctk.CTkFrame):
    def __init__(self, master, width=70, height=70, image=None, **kwargs):
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

        # 🔥 keep reference
        self.image = image

        if image:
            self.label = ctk.CTkLabel(self, image=self.image, text="")
            self.label.place(relx=0.5, rely=0.5, anchor="center")
