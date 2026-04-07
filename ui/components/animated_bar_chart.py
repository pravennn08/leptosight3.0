import customtkinter as ctk
import math
from collections import Counter


class AnimatedBarChart(ctk.CTkFrame):

    def __init__(
        self, master, title="Bar Chart", lines_config=None, bg="#F8FAFC", **kwargs
    ):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.lines_config = lines_config or []
        self.full_data = []

        # CONTAINER (MATCH LINE CHART)
        self.chart_container = ctk.CTkFrame(self, fg_color="transparent")
        self.chart_container.pack(fill="both", expand=True, padx=30, pady=30)

        # HEADER
        self.header_frame = ctk.CTkFrame(self.chart_container, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=20, pady=(10, 0))

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text=title,
            font=("Inter", 23),
            text_color="#111827",
        )
        self.title_label.pack(side="left")

        self.filter_var = ctk.StringVar(value="All")

        self.filter_menu = ctk.CTkOptionMenu(
            self.header_frame,
            values=["All"] + [l["label"] for l in self.lines_config],
            variable=self.filter_var,
            command=self.on_filter_change,
            width=180,
            height=36,
            font=("Inter", 18),
            fg_color="#0EA5E9",  # main blue
            button_color="#0284C7",  # darker blue
            button_hover_color="#0369A1",
            text_color="#FFFFFF",
            dropdown_fg_color="#FFFFFF",
            dropdown_text_color="#0F172A",
            dropdown_hover_color="#E2E8F0",
            dropdown_font=("Inter", 18),
            corner_radius=9,
        )
        self.filter_menu.pack(side="right")

        # CANVAS
        self.canvas = ctk.CTkCanvas(self.chart_container, bg=bg, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=20)

    # UPDATE
    def update_chart(self, data):
        self.full_data = data
        self.apply_filter()

    def apply_filter(self):
        selected = self.filter_var.get()

        # Aggregate values per classification
        result = {}

        for d in self.full_data:
            key = d["classification"]
            value = d.get("value", 0)

            result[key] = result.get(key, 0) + value

        if selected == "All":
            filtered = result
        else:
            filtered = {selected: result.get(selected, 0)}

        self.draw_chart(filtered)

    def on_filter_change(self, choice):
        self.apply_filter()

    # DRAW
    def draw_chart(self, data):

        self.canvas.delete("all")

        if not data:
            return

        labels = list(data.keys())
        values = list(data.values())

        self.update_idletasks()

        W = max(self.canvas.winfo_width(), 650)
        H = max(self.canvas.winfo_height(), 350)

        left_pad = 60
        right_pad = 60
        top_pad = 50
        bottom_pad = 90

        chart_width = W - left_pad - right_pad
        chart_height = H - top_pad - bottom_pad

        max_value = max(values)
        scale_max = max(5, math.ceil(max_value / 5) * 5)

        steps = 5

        # GRID
        for i in range(steps + 1):
            y = top_pad + (chart_height / steps) * i
            value = scale_max - (scale_max / steps) * i

            self.canvas.create_line(left_pad, y, W - right_pad, y, fill="#E5E7EB")

            self.canvas.create_text(
                30,
                y,
                text=f"{int(value)}",
                fill="#94A3B8",
                font=("Segoe UI", 13),
            )

        # BAR SETTINGS
        bar_width = 80
        spacing = chart_width / (len(values) if len(values) > 0 else 1)

        bars = []

        for i, label in enumerate(labels):
            value = values[i]

            x_center = left_pad + spacing * i + spacing / 2
            x0 = x_center - bar_width / 2
            x1 = x_center + bar_width / 2

            y_bottom = H - bottom_pad

            # Match color from config
            color = next(
                (l["color"] for l in self.lines_config if l["label"] == label),
                "#2563EB",
            )

            rect = self.canvas.create_rectangle(
                x0, y_bottom, x1, y_bottom, fill=color, width=0
            )

            # X labels
            self.canvas.create_text(
                x_center,
                H - 40,
                text=label,
                fill="#64748B",
                font=("Segoe UI", 12),
            )

            txt = self.canvas.create_text(
                x_center,
                y_bottom - 10,
                text="0",
                font=("Segoe UI", 12),
            )

            bars.append((rect, txt, value, x0, x1, y_bottom))

        # ANIMATION
        frames = 60
        duration = 12

        def animate(frame=0):

            progress = frame / frames
            ease = 1 - (1 - progress) ** 3

            for rect, txt, value, x0, x1, yb in bars:

                target_h = (value / scale_max) * chart_height
                current_h = target_h * ease

                top_y = yb - current_h

                self.canvas.coords(rect, x0, top_y, x1, yb)
                self.canvas.coords(txt, (x0 + x1) / 2, top_y - 10)

                self.canvas.itemconfig(txt, text=str(int(value * ease)))

            if frame < frames:
                self.after(duration, lambda: animate(frame + 1))

        animate()

        # LEGEND (MATCH LINE CHART)
        legend_y = H - 10
        font = ("Segoe UI", 12)

        box = 12
        gap = 8
        padding = 20

        text_widths = []

        for line in self.lines_config:
            temp = self.canvas.create_text(
                0, 0, text=line["label"], font=font, anchor="nw"
            )
            bbox = self.canvas.bbox(temp)
            self.canvas.delete(temp)
            text_widths.append(bbox[2] - bbox[0])

        total_width = sum(box + gap + w + padding for w in text_widths) - padding
        start_x = (W - total_width) / 2

        x = start_x

        for i, line in enumerate(self.lines_config):
            self.canvas.create_rectangle(
                x, legend_y - 8, x + box, legend_y + 4, fill=line["color"], width=0
            )
            x += box + gap

            self.canvas.create_text(
                x, legend_y, text=line["label"], anchor="w", fill="#334155", font=font
            )

            x += text_widths[i] + padding
