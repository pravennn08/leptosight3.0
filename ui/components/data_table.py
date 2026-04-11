import customtkinter as ctk


class DataTable(ctk.CTkFrame):

    def __init__(
        self,
        master,
        headers,
        data,
        actions=None,
        table_width=None,
        header_color=None,
        row_color=None,
        **kwargs,
    ):
        super().__init__(master, fg_color="white", **kwargs, corner_radius=10)

        self.headers = headers
        self.data = data
        self.actions = actions or []
        self.table_width = table_width
        self.header_color = header_color
        self.row_color = row_color
        self.rows = []

        self.build_table()

    # BUILD TABLE
    def build_table(self):

        self.draw_headers()
        self.draw_rows()

    # HEADER LOOP
    def draw_headers(self):

        for col, text in enumerate(self.headers):

            lbl = ctk.CTkLabel(
                self,
                text=text,
                fg_color=self.header_color,
                text_color="#FFFFFF",
                height=75,
                corner_radius=0,
                font=("Inter", 16, "bold"),
                width=self.table_width,
            )

            lbl.grid(row=0, column=col, sticky="nsew", padx=0)

    # ROW LOOP
    def draw_rows(self):

        for row, item in enumerate(self.data, start=1):

            # ROW COLOR
            color = "#FFFFFF" if row % 2 == 0 else "#F3F4F6"

            # STORE ALL WIDGETS OF THIS ROW
            row_widgets = []

            # NORMAL COLUMNS
            for col, value in enumerate(item):

                lbl = ctk.CTkLabel(
                    self,
                    text=str(value),
                    fg_color=color,
                    height=70,
                    padx=10,
                    width=self.table_width,
                    font=("Poppins", 15),
                )

                lbl.grid(row=row, column=col, sticky="nsew")
                lbl.bind("<Button-1>", lambda e, r=row: self.select_row(r))

                row_widgets.append(lbl)

            # ACTION COLUMN
            if self.actions:

                action_frame = ctk.CTkFrame(
                    self,
                    fg_color=color,
                    bg_color=color,
                )

                action_frame.grid(
                    row=row,
                    column=len(self.headers) - 1,
                    sticky="nsew",
                    columnspan=2,
                )

                action_frame.bind("<Button-1>", lambda e, r=row: self.select_row(r))

                row_widgets.append(action_frame)

                for action in self.actions:

                    btn = ctk.CTkButton(
                        action_frame,
                        text=action.get("text", ""),
                        font=("Inter", 15, "bold"),
                        image=action.get("icon", None),
                        compound="left",
                        width=100,
                        height=45,
                        fg_color=action.get("color", "#3B82F6"),
                        hover_color=action.get("hover", "#2563EB"),
                        text_color="#FFFFFF",
                        command=lambda idx=row - 1, func=action["command"]: func(idx),
                    )

                    btn.pack(side="left", padx=5)

            # SAVE THE WHOLE ROW
            self.rows.append((row, row_widgets))

    # def update_data(self, new_data):
    #     # Update internal data
    #     self.data = new_data

    #     if self.data == new_data:
    #         return  # skip redraw

    #     # ❌ Remove ONLY row widgets (keep headers at row=0)
    #     for widget in self.grid_slaves():
    #         info = widget.grid_info()
    #         if int(info["row"]) > 0:  # skip header row
    #             widget.destroy()

    #     # Reset stored rows
    #     self.rows = []

    #     # ✅ Redraw rows with new data
    #     self.draw_rows()

    def update_data(self, new_data):
        # ✅ Compare FIRST
        if self.data == new_data:
            return  # skip redraw

        # Then update
        self.data = new_data

        # Remove only row widgets
        for widget in self.grid_slaves():
            info = widget.grid_info()
            if int(info["row"]) > 0:
                widget.destroy()

        # Reset stored rows
        self.rows = []

        # Redraw rows
        self.draw_rows()

    def select_row(self, selected_row):

        for row, widgets in self.rows:

            default_color = "#FFFFFF" if row % 2 == 0 else "#F3F4F6"
            color = "#E6F0FF" if row == selected_row else default_color
            for w in widgets:
                w.configure(fg_color=color)
