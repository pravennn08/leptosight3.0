import customtkinter as ctk
import math


class AnimatedResultLineChart(ctk.CTkFrame):

    def __init__(self, master, title="Historic Progress", bg="#E2E8F0", **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.full_data = []

        # 🎨 3 LINES CONFIG
        self.lines_config = [
            {"key": "temp", "label": "Temperature", "color": "#F59E0B"},  # yellow
            {"key": "test", "label": "Test Confidence", "color": "#EC4899"},  # pink
            {"key": "eye", "label": "Eye Confidence", "color": "#8B5CF6"},  # violet
        ]

        # ================= CONTAINER =================
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=15, pady=15)

        # ================= HEADER =================
        self.header = ctk.CTkFrame(self.container, fg_color="transparent")
        self.header.pack(fill="x", pady=(5, 5))

        self.title_label = ctk.CTkLabel(
            self.header,
            text=title,
            font=("Inter", 18.5),
            text_color="#0F172A",
        )
        self.title_label.pack(side="left")

        # 🔥 FILTER MENU
        self.filter_var = ctk.StringVar(value="All Sessions")

        self.filter_menu = ctk.CTkOptionMenu(
            self.header,
            values=["All Sessions", "Last 3 Sessions", "Last 5 Sessions"],
            variable=self.filter_var,
            command=self.on_filter_change,
            width=170,
            height=34,
            font=("Inter", 16),
            fg_color="#14B8A6",
            button_color="#0D9488",
            dropdown_fg_color="#FFFFFF",
            dropdown_text_color="#0F172A",
            dropdown_hover_color="#D4D6DA",
            dropdown_font=("Inter", 16),
            text_color="#FFFFFF",
            corner_radius=9,
        )
        self.filter_menu.pack(side="right")

        # ================= CANVAS =================
        self.canvas = ctk.CTkCanvas(self.container, bg=bg, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

    # ================= UPDATE =================
    def update_chart(self, data):
        self.full_data = data
        self.apply_filter()

    def apply_filter(self):
        data = self.full_data
        selected = self.filter_var.get()

        if selected == "Last 3 Sessions":
            data = data[-3:]
        elif selected == "Last 5 Sessions":
            data = data[-5:]

        self.draw_chart(data)

    def on_filter_change(self, choice):
        self.apply_filter()

    # ================= DRAW =================
    def draw_chart(self, data):
        self.canvas.delete("all")

        if not data:
            return

        labels = [d["session"] for d in data]

        # 🔥 Collect values per line
        line_values = {
            line["key"]: [d[line["key"]] for d in data] for line in self.lines_config
        }

        self.update_idletasks()

        W = max(self.canvas.winfo_width(), 450)
        H = max(self.canvas.winfo_height(), 320)

        left_pad = 50
        right_pad = 30
        top_pad = 30
        bottom_pad = 80

        chart_width = W - left_pad - right_pad
        chart_height = H - top_pad - bottom_pad

        max_value = max(max(v) for v in line_values.values())
        scale_max = max(100, math.ceil(max_value / 10) * 10)

        steps = 5

        # ===== GRID =====
        for i in range(steps + 1):
            y = top_pad + (chart_height / steps) * i
            value = scale_max - (scale_max / steps) * i

            self.canvas.create_line(
                left_pad,
                y,
                W - right_pad,
                y,
                fill="#CBD5E1",
            )

            self.canvas.create_text(
                25, y, text=f"{int(value)}", fill="#94A3B8", font=("Segoe UI", 10)
            )

        # ===== X POSITIONS =====
        step_x = chart_width / (len(data) - 1 if len(data) > 1 else 1)

        def get_points(values):
            pts = []
            for i, value in enumerate(values):
                x = left_pad + i * step_x
                y = top_pad + chart_height - (value / scale_max) * chart_height
                pts.append((x, y))

                self.canvas.create_text(
                    x - 10,
                    H - 35,
                    text=labels[i],
                    fill="#64748B",
                    font=("Segoe UI", 10),
                )
            return pts

        all_points = {
            line["key"]: get_points(line_values[line["key"]])
            for line in self.lines_config
        }

        # ===== DOTS =====
        def create_dots(points, color):
            return [
                self.canvas.create_oval(x, y, x, y, fill=color, width=0)
                for x, y in points
            ]

        all_dots = {
            line["key"]: create_dots(all_points[line["key"]], line["color"])
            for line in self.lines_config
        }

        # ===== LINES =====
        def create_lines(points, color):
            return [
                self.canvas.create_line(
                    points[i][0],
                    points[i][1],
                    points[i][0],
                    points[i][1],
                    fill=color,
                    width=3,
                    smooth=True,
                )
                for i in range(len(points) - 1)
            ]

        all_lines = {
            line["key"]: create_lines(all_points[line["key"]], line["color"])
            for line in self.lines_config
        }

        # ===== ANIMATION =====
        frames = 60
        duration = 12

        def animate(frame=0):
            progress = frame / frames
            ease = 1 - (1 - progress) ** 3  # smooth easing

            for line in self.lines_config:
                key = line["key"]
                pts = all_points[key]
                lines = all_lines[key]
                dots = all_dots[key]

                total = len(pts)
                current = ease * (total - 1)

                index = int(current)
                t = current - index  # fractional part (important!)

                # 🔥 Animate lines smoothly
                for i in range(len(lines)):
                    if i < index:
                        # fully drawn segments
                        self.canvas.coords(
                            lines[i],
                            pts[i][0],
                            pts[i][1],
                            pts[i + 1][0],
                            pts[i + 1][1],
                        )

                    elif i == index and i < total - 1:
                        # 🔥 PARTIAL segment (this is the key fix)
                        x1, y1 = pts[i]
                        x2, y2 = pts[i + 1]

                        xi = x1 + (x2 - x1) * t
                        yi = y1 + (y2 - y1) * t

                        self.canvas.coords(
                            lines[i],
                            x1,
                            y1,
                            xi,
                            yi,
                        )

                # 🔥 Animate dots smoothly
                for i, (x, y) in enumerate(pts):
                    if i <= index:
                        r = 4
                        self.canvas.coords(dots[i], x - r, y - r, x + r, y + r)

            if frame < frames:
                self.after(duration, lambda: animate(frame + 1))

        animate()
        legend_y = H - 15

        box_size = 12
        gap = 6  # space between box and text
        item_spacing = 20  # space between legend items
        font = ("Segoe UI", 10)

        # 🔥 Measure text widths
        text_widths = []
        for line in self.lines_config:
            temp = self.canvas.create_text(
                0, 0, text=line["label"], font=font, anchor="nw"
            )
            bbox = self.canvas.bbox(temp)
            self.canvas.delete(temp)
            text_widths.append(bbox[2] - bbox[0])

        # 🔥 Compute total width
        total_width = (
            sum(
                box_size + gap + text_widths[i] + item_spacing
                for i in range(len(self.lines_config))
            )
            - item_spacing
        )  # remove last extra spacing

        # 🔥 Center start position
        x = (W - total_width) / 2

        # 🔥 Draw legend
        for i, line in enumerate(self.lines_config):

            # color box
            self.canvas.create_rectangle(
                x, legend_y - 8, x + box_size, legend_y + 4, fill=line["color"], width=0
            )
            x += box_size + gap

            # label
            self.canvas.create_text(
                x,
                legend_y,
                text=line["label"],
                anchor="w",
                fill="#334155",
                font=font,
            )
            x += text_widths[i] + item_spacing
