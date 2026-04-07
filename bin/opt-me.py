#     # self.roles = ["Patient", "Personnel", "Admin"]

#     # self.selected_role = ctk.StringVar(value="")
#     # self.options_frame = ctk.CTkFrame(self.container, fg_color="transparent")
#     # self.options_frame.place(x=30, y=430)

#     # self.cards = []

#     # for idx, choice in enumerate(self.roles):
#     #     card = ctk.CTkFrame(
#     #         self.options_frame,
#     #         fg_color="#F8FAFC",
#     #         border_color="#E2E8F0",
#     #         corner_radius=9,
#     #         border_width=2,
#     #         width=128,
#     #         height=38,
#     #     )
#     #     card.pack(side="left", padx=5)
#     #     card.pack_propagate(False)

#     #     # CLICK CARD
#     #     card.bind("<Button-1>", lambda e, i=idx, c=card: self.select_role(i, c))

#     #     # RADIO BUTTON
#     #     rb = ctk.CTkRadioButton(
#     #         card,
#     #         text=choice,
#     #         value=str(idx),
#     #         variable=self.selected_role,
#     #         fg_color=PRIMARY,
#     #         font=("Roboto", 15),
#     #         text_color=TEXT_SECONDARY,
#     #         radiobutton_height=10,
#     #         command=lambda i=idx, c=card: self.select_role(i, c),
#     #     )
#     #     rb.pack(expand=True)
#     #     self.cards.append(card)
