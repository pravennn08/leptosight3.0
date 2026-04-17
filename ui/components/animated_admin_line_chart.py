import customtkinter as ctk
import math

# ✅ YOUR COLORS
GREEN = "#14B8A6"
VIOLET = "#8B5CF6"
YELLOW = "#F59E0B"
ORANGE = "#f1c40f"
RED = "#EF4444"
PINK = "#EC4899"
BLUE = "#0EA5E9"


class AnimatedAdminLineChart(ctk.CTkFrame):

    def __init__(self, master, title="Weekly Users (Mon–Sun)", bg="#E2E8F0", **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.title = title
        self.full_data = []

        # ✅ DAYS + COLORS
        self.days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        self.day_colors = {
            "Mon": GREEN,
            "Tue": BLUE,
            "Wed": PINK,
            "Thu": VIOLET,
            "Fri": YELLOW,
            "Sat": ORANGE,
            "Sun": RED,
        }

        # CONTAINER
        self.chart_container = ctk.CTkFrame(self, fg_color="transparent")
        self.chart_container.pack(fill="both", expand=True, padx=30, pady=30)

        # HEADER
        self.header_frame = ctk.CTkFrame(self.chart_container, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=20, pady=(10, 0))

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text=self.title,
            font=("Inter", 22),
            text_color="#111827",
        )
        self.title_label.pack(side="left")

        # ✅ FILTER MENU
        self.filter_var = ctk.StringVar(value="All Days")

        self.filter_menu = ctk.CTkOptionMenu(
            self.header_frame,
            values=["All Days", "Last 3 Days", "Last 5 Days"],
            variable=self.filter_var,
            command=self.on_filter_change,
            width=180,
            height=36,
            font=("Inter", 18),
            fg_color=GREEN,
            button_color="#0D9488",
            button_hover_color="#13857B",
            text_color="#FFFFFF",
            dropdown_fg_color="#FFFFFF",
            dropdown_text_color="#0F172A",
            dropdown_hover_color="#D4D6DA",
            dropdown_font=("Inter", 18),
            corner_radius=9,
        )
        self.filter_menu.pack(side="right")

        # CANVAS
        self.canvas = ctk.CTkCanvas(self.chart_container, bg=bg, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=20)

    # =========================
    # UPDATE + FILTER
    # =========================
    def update_chart(self, data):
        self.full_data = data
        self.apply_filter()

    def on_filter_change(self, choice):
        self.apply_filter()

    def apply_filter(self):
        data = self.full_data
        selected = self.filter_var.get()

        if selected == "Last 3 Days":
            data = data[-3:]
        elif selected == "Last 5 Days":
            data = data[-5:]

        self.draw_chart(data)

    # =========================
    # DRAW
    # =========================
    def draw_chart(self, data):
        self.canvas.delete("all")

        if not data:
            return

        labels = [d["day"] for d in data]
        values = [d["users"] for d in data]

        self.update_idletasks()

        W = max(self.canvas.winfo_width(), 650)
        H = max(self.canvas.winfo_height(), 350)

        left_pad = 60
        right_pad = 60
        top_pad = 50
        bottom_pad = 90

        chart_width = W - left_pad - right_pad
        chart_height = H - top_pad - bottom_pad

        max_value = max(values) if values else 0
        scale_max = max(10, math.ceil(max_value / 5) * 5)

        steps = 5

        # GRID
        for i in range(steps + 1):
            y = top_pad + (chart_height / steps) * i
            value = scale_max - (scale_max / steps) * i

            # self.canvas.create_line(left_pad, y, W - right_pad, y, fill="#EEEFF3")
            self.canvas.create_line(
                left_pad, y, W - right_pad, y, fill="#CBD5E1", width=1  # ✅ best match
            )

            self.canvas.create_text(
                30,
                y,
                text=f"{int(value)}",
                fill="#94A3B8",
                font=("Segoe UI", 13),
            )

        step_x = chart_width / (len(data) - 1 if len(data) > 1 else 1)

        # POINTS
        points = []
        for i, value in enumerate(values):
            x = left_pad + i * step_x
            y = top_pad + chart_height - (value / scale_max) * chart_height
            points.append((x, y))

            # X LABEL
            self.canvas.create_text(
                x - 5,
                H - 40,
                text=labels[i],
                fill="#64748B",
                font=("Segoe UI", 12),
            )

        # DOTS (colored per day)
        dots = []
        for i, (x, y) in enumerate(points):
            color = self.day_colors.get(labels[i], GREEN)
            dot = self.canvas.create_oval(x, y, x, y, fill=color, width=0)
            dots.append(dot)

        # LINES (colored per segment)
        lines = []
        for i in range(len(points) - 1):
            color = self.day_colors.get(labels[i], GREEN)

            line = self.canvas.create_line(
                points[i][0],
                points[i][1],
                points[i][0],
                points[i][1],
                fill=color,
                width=3,
                smooth=True,
            )
            lines.append(line)

        # ANIMATION
        frames = 60
        duration = 12

        def animate(frame=0):
            progress = frame / frames
            ease = 1 - (1 - progress) ** 3

            visible_points = int(ease * (len(points) - 1))

            for i in range(len(lines)):
                if i < visible_points:
                    self.canvas.coords(
                        lines[i],
                        points[i][0],
                        points[i][1],
                        points[i + 1][0],
                        points[i + 1][1],
                    )
                elif i == visible_points and i < len(points) - 1:
                    x0, y0 = points[i]
                    x1, y1 = points[i + 1]

                    x = x0 + (x1 - x0) * (ease * (len(points) - 1) - i)
                    y = y0 + (y1 - y0) * (ease * (len(points) - 1) - i)

                    self.canvas.coords(lines[i], x0, y0, x, y)

            for i, (x, y) in enumerate(points):
                if i <= visible_points:
                    r = 4
                    self.canvas.coords(dots[i], x - r, y - r, x + r, y + r)

            if frame < frames:
                self.after(duration, lambda: animate(frame + 1))

        animate()

        # =========================
        # LEGEND
        # =========================
        legend_y = H - 10
        font = ("Segoe UI", 12)

        box = 12
        gap = 8
        padding = 20

        legend_config = [
            {"label": day, "color": self.day_colors[day]} for day in self.days
        ]

        text_widths = []

        for item in legend_config:
            temp = self.canvas.create_text(
                0, 0, text=item["label"], font=font, anchor="nw"
            )
            bbox = self.canvas.bbox(temp)
            self.canvas.delete(temp)
            text_widths.append(bbox[2] - bbox[0])

        total_width = sum(box + gap + w + padding for w in text_widths) - padding
        start_x = (W - total_width) / 2

        x = start_x

        for i, item in enumerate(legend_config):
            self.canvas.create_rectangle(
                x, legend_y - 8, x + box, legend_y + 4, fill=item["color"], width=0
            )
            x += box + gap

            self.canvas.create_text(
                x, legend_y, text=item["label"], anchor="w", fill="#334155", font=font
            )

            x += text_widths[i] + padding
