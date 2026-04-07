import customtkinter as ctk
import math


class AnimatedHorizontalBarChart(ctk.CTkFrame):
    def __init__(
        self, master, title="Patient Factors", lines_config=None, bg="#F8FAFC", **kwargs
    ):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.lines_config = lines_config or []
        self.full_data = []

        # ===== CONTAINER (OPTIMIZED FOR 540x380) =====
        self.chart_container = ctk.CTkFrame(self, fg_color="transparent")
        self.chart_container.pack(fill="both", expand=True, padx=15, pady=15)

        # ===== HEADER =====
        self.header_frame = ctk.CTkFrame(self.chart_container, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(5, 5))

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text=title,
            font=("Inter", 20),
            text_color="#0F172A",
        )
        self.title_label.pack(side="left")

        # ===== CANVAS =====
        self.canvas = ctk.CTkCanvas(self.chart_container, bg=bg, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

    # ===== UPDATE =====
    def update_chart(self, data):
        self.full_data = data
        self.draw_chart()

    def draw_chart(self):
        self.canvas.delete("all")

        if not self.full_data:
            return

        labels = [d["feature"] for d in self.full_data]
        values = [d["score"] for d in self.full_data]

        self.update_idletasks()

        W = max(self.canvas.winfo_width(), 800)
        H = max(self.canvas.winfo_height(), 320)

        # 🔥 RESERVE SPACE FOR LEGEND
        legend_width = 160

        left_pad = 140
        right_pad = legend_width - 100  # 🔥 reserve right space
        top_pad = 20
        bottom_pad = 20

        chart_width = W - left_pad - right_pad + 200
        chart_height = H - top_pad - bottom_pad

        max_value = max(values)
        scale_max = max_value * 1.05 + 20

        # ===== BAR SETTINGS =====
        row_height = chart_height / len(values)
        bar_height = min(18, row_height * 0.5) + 25

        bars = []

        for i, label in enumerate(labels):
            value = values[i]

            y_center = top_pad + (i * row_height) + row_height / 2

            y0 = y_center - bar_height / 2
            y1 = y_center + bar_height / 2

            # COLOR
            color = next(
                (l["color"] for l in self.lines_config if l["label"] == label),
                "#14B8A6",
            )

            rect = self.canvas.create_rectangle(
                left_pad, y0, left_pad, y1, fill=color, width=0
            )

            # LEFT LABEL
            self.canvas.create_text(
                20,
                y_center,
                text=label.replace("_", " ").title(),
                anchor="w",
                fill="#475569",
                font=("Segoe UI", 12),
            )

            # VALUE
            txt = self.canvas.create_text(
                left_pad + 5,
                y_center,
                text="0.00",
                anchor="w",
                fill="#0F172A",
                font=("Segoe UI", 11, "bold"),
            )

            bars.append((rect, txt, value, y0, y1))

        # ===== ANIMATION =====
        frames = 50
        duration = 10

        def animate(frame=0):
            progress = frame / frames
            ease = 1 - (1 - progress) ** 3

            for rect, txt, value, y0, y1 in bars:
                current_val = value * ease
                # bar_length = (current_val / scale_max) * chart_width
                min_width = 10  # minimum pixels
                bar_length = max((current_val / scale_max) * chart_width, min_width)

                x1 = left_pad + bar_length

                self.canvas.coords(rect, left_pad, y0, x1, y1)
                self.canvas.coords(txt, x1 + 8, (y0 + y1) / 2)

                self.canvas.itemconfig(txt, text=f"{current_val:.2f}")

            if frame < frames:
                self.after(duration, lambda: animate(frame + 1))

        animate()

        # ===== 🔥 VERTICAL LEGEND (RIGHT SIDE) =====
        legend_x = W - legend_width + 150
        legend_y = top_pad + 10
        spacing = 28

        for i, item in enumerate(self.lines_config):
            y = legend_y + i * spacing

            # COLOR BOX
            self.canvas.create_rectangle(
                legend_x, y, legend_x + 12, y + 12, fill=item["color"], width=0
            )

            # LABEL TEXT
            self.canvas.create_text(
                legend_x + 18,
                y + 6,
                text=item["label"].replace("_", " ").title(),
                anchor="w",
                fill="#334155",
                font=("Segoe UI", 11),
            )
