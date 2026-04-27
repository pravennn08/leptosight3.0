# import customtkinter as ctk


# import math


# class AnimatedHorizontalBarChart(ctk.CTkFrame):
#     def __init__(
#         self, master, title="Patient Factors", lines_config=None, bg="#E2E8F0", **kwargs
#     ):
#         super().__init__(master, fg_color="transparent", **kwargs)

#         self.lines_config = lines_config or []
#         self.full_data = []

#         # ===== CONTAINER (OPTIMIZED FOR 540x380) =====
#         self.chart_container = ctk.CTkFrame(self, fg_color="transparent")
#         self.chart_container.pack(fill="both", expand=True, padx=15, pady=15)

#         # ===== HEADER =====
#         self.header_frame = ctk.CTkFrame(self.chart_container, fg_color="transparent")
#         self.header_frame.pack(fill="x", pady=(5, 5))

#         self.title_label = ctk.CTkLabel(
#             self.header_frame,
#             text=title,
#             font=("Inter", 20),
#             text_color="#0F172A",
#         )
#         self.title_label.pack(side="left")

#         # ===== CANVAS =====
#         self.canvas = ctk.CTkCanvas(self.chart_container, bg=bg, highlightthickness=0)
#         self.canvas.pack(fill="both", expand=True)

#     # ===== UPDATE =====
#     def update_chart(self, data):
#         self.full_data = data
#         self.draw_chart()

#     def draw_chart(self):
#         self.canvas.delete("all")

#         if not self.full_data:
#             return

#         labels = [d["feature"] for d in self.full_data]
#         values = [d["score"] for d in self.full_data]

#         self.update_idletasks()

#         W = max(self.canvas.winfo_width(), 450)
#         H = max(self.canvas.winfo_height(), 350)

#         # 🔥 RESERVE SPACE FOR LEGEND
#         legend_width = 160

#         left_pad = 140
#         right_pad = legend_width - 100  # 🔥 reserve right space
#         top_pad = 20
#         bottom_pad = 20

#         chart_width = W - left_pad - right_pad + 200
#         chart_height = H - top_pad - bottom_pad

#         max_value = max(values)
#         scale_max = max_value * 1.05 + 20

#         # ===== BAR SETTINGS =====
#         row_height = chart_height / len(values)
#         bar_height = min(18, row_height * 0.5) + 15

#         bars = []

#         for i, label in enumerate(labels):
#             value = values[i]

#             y_center = top_pad + (i * row_height) + row_height / 2

#             y0 = y_center - bar_height / 2
#             y1 = y_center + bar_height / 2

#             # COLOR
#             color = next(
#                 (l["color"] for l in self.lines_config if l["label"] == label),
#                 "#14B8A6",
#             )

#             rect = self.canvas.create_rectangle(
#                 left_pad, y0, left_pad, y1, fill=color, width=0
#             )

#             # LEFT LABEL
#             self.canvas.create_text(
#                 20,
#                 y_center,
#                 text=label.replace("_", " ").title(),
#                 anchor="w",
#                 fill="#475569",
#                 font=("Segoe UI", 11),
#             )

#             # VALUE
#             txt = self.canvas.create_text(
#                 left_pad + 5,
#                 y_center,
#                 text="0.00",
#                 anchor="w",
#                 fill="#0F172A",
#                 font=("Segoe UI", 11, "bold"),
#             )

#             bars.append((rect, txt, value, y0, y1))

#         # ===== ANIMATION =====
#         frames = 50
#         duration = 10

#         def animate(frame=0):
#             progress = frame / frames
#             ease = 1 - (1 - progress) ** 3

#             for rect, txt, value, y0, y1 in bars:
#                 current_val = value * ease
#                 # bar_length = (current_val / scale_max) * chart_width
#                 min_width = 10  # minimum pixels
#                 bar_length = max((current_val / scale_max) * chart_width, min_width)

#                 x1 = left_pad + bar_length

#                 self.canvas.coords(rect, left_pad, y0, x1, y1)
#                 self.canvas.coords(txt, x1 + 8, (y0 + y1) / 2)

#                 self.canvas.itemconfig(txt, text=f"{current_val:.2f}")

#             if frame < frames:
#                 self.after(duration, lambda: animate(frame + 1))

#         animate()

#         # LEGEND VERTICAL HERE WITH PROPER PADDING

#         # ===== LEGEND (BOTTOM CENTERED - PROPER PADDING) =====

#         legend_y = H - 15

#         box_size = 12
#         gap = 6
#         item_spacing = 12
#         font = ("Segoe UI", 10)

#         # 🔥 Measure text widths
#         text_widths = []
#         for item in self.lines_config:
#             temp = self.canvas.create_text(
#                 0, 0, text=item["label"], font=font, anchor="nw"
#             )
#             bbox = self.canvas.bbox(temp)
#             self.canvas.delete(temp)
#             text_widths.append(bbox[2] - bbox[0])

#         # 🔥 Compute total width (for centering)
#         total_width = (
#             sum(
#                 box_size + gap + text_widths[i] + item_spacing
#                 for i in range(len(self.lines_config))
#             )
#             - item_spacing
#         )

#         # 🔥 Start centered
#         x = (W - total_width) / 2

#         # 🔥 Draw legend row
#         for i, item in enumerate(self.lines_config):

#             # color box
#             self.canvas.create_rectangle(
#                 x, legend_y - 8, x + box_size, legend_y + 4, fill=item["color"], width=0
#             )
#             x += box_size + gap

#             # label
#             self.canvas.create_text(
#                 x,
#                 legend_y,
#                 text=item["label"].replace("_", " ").title(),
#                 anchor="w",
#                 fill="#334155",
#                 font=font,
#             )
#             x += text_widths[i] + item_spacing


# import customtkinter as ctk
# import math


# class AnimatedHorizontalBarChart(ctk.CTkFrame):
#     def __init__(
#         self, master, title="Patient Factors", lines_config=None, bg="#E2E8F0", **kwargs
#     ):
#         super().__init__(master, fg_color="transparent", **kwargs)

#         self.lines_config = lines_config or []
#         self.full_data = []

#         self.chart_container = ctk.CTkFrame(self, fg_color="transparent")
#         self.chart_container.pack(fill="both", expand=True, padx=15, pady=15)

#         self.header_frame = ctk.CTkFrame(self.chart_container, fg_color="transparent")
#         self.header_frame.pack(fill="x", pady=(5, 5))

#         self.title_label = ctk.CTkLabel(
#             self.header_frame,
#             text=title,
#             font=("Inter", 20),
#             text_color="#0F172A",
#         )
#         self.title_label.pack(side="left")

#         self.canvas = ctk.CTkCanvas(self.chart_container, bg=bg, highlightthickness=0)
#         self.canvas.pack(fill="both", expand=True)

#     def update_chart(self, data):
#         self.full_data = data
#         self.draw_chart()

#     def draw_chart(self):
#         self.canvas.delete("all")

#         if not self.full_data:
#             return

#         labels = [d["feature"] for d in self.full_data]
#         values = [d["score"] for d in self.full_data]

#         self.update_idletasks()

#         W = max(self.canvas.winfo_width(), 450)
#         H = max(self.canvas.winfo_height(), 350)

#         left_pad = 140
#         right_pad = 40
#         top_pad = 30
#         bottom_pad = 70

#         chart_width = W - left_pad - right_pad
#         chart_height = H - top_pad - bottom_pad

#         # 🔥 SHAP scaling (absolute max)
#         scale_max = max(abs(v) for v in values) or 1 * 1.5

#         # 🔥 CENTER LINE (0 baseline)
#         center_x = left_pad + chart_width / 2

#         self.canvas.create_line(
#             center_x,
#             top_pad,
#             center_x,
#             H - bottom_pad,
#             fill="#94A3B8",
#             dash=(4, 2),
#         )

#         # ===== BAR SETTINGS =====
#         row_height = chart_height / len(values)
#         bar_height = min(18, row_height * 0.5) + 20

#         bars = []

#         for i, label in enumerate(labels):
#             value = values[i]

#             y_center = top_pad + (i * row_height) + row_height / 2

#             y0 = y_center - bar_height / 2
#             y1 = y_center + bar_height / 2

#             # 🔥 SHAP COLORS
#             color = "#2563EB" if value >= 0 else "#EF4444"

#             rect = self.canvas.create_rectangle(
#                 center_x, y0, center_x, y1, fill=color, width=0
#             )

#             # LEFT LABEL
#             self.canvas.create_text(
#                 20,
#                 y_center,
#                 text=label.replace("_", " ").title(),
#                 anchor="w",
#                 fill="#475569",
#                 font=("Segoe UI", 11),
#             )

#             txt = self.canvas.create_text(
#                 center_x,
#                 y_center,
#                 text="",
#                 anchor="w",
#                 fill="#0F172A",
#                 font=("Segoe UI", 10, "bold"),
#             )

#             bars.append((rect, txt, value, y0, y1))

#         # ===== ANIMATION =====
#         frames = 50
#         duration = 10

#         def animate(frame=0):
#             progress = frame / frames
#             ease = 1 - (1 - progress) ** 3

#             for rect, txt, value, y0, y1 in bars:
#                 current_val = value * ease

#                 bar_length = (abs(current_val) / scale_max) * (chart_width / 2)

#                 if value >= 0:
#                     x0 = center_x
#                     x1 = center_x + bar_length
#                     text_x = x1 + 8
#                 else:
#                     x0 = center_x - bar_length
#                     x1 = center_x
#                     text_x = x0 - 8

#                 self.canvas.coords(rect, x0, y0, x1, y1)
#                 self.canvas.coords(txt, text_x, (y0 + y1) / 2)

#                 sign = "+" if value >= 0 else "−"
#                 self.canvas.itemconfig(txt, text=f"{sign}{abs(current_val):.2f}")

#             if frame < frames:
#                 self.after(duration, lambda: animate(frame + 1))

#         animate()

#         # ===== SHAP X-AXIS LABELS =====
#         self.canvas.create_text(
#             left_pad,
#             H - 25,
#             text="E[f(X)]",
#             fill="#64748B",
#             font=("Segoe UI", 10),
#         )

#         self.canvas.create_text(
#             W - right_pad,
#             H - 25,
#             text="f(x)",
#             fill="#64748B",
#             font=("Segoe UI", 10),
#         )

#         # ===== LEGEND =====
#         legend_y = H - 10

#         items = [
#             ("Supports Prediction", "#2563EB"),
#             ("Opposes Prediction", "#EF4444"),
#         ]

#         box = 12
#         gap = 6
#         spacing = 40

#         total_width = len(items) * 160
#         x = (W - total_width) / 2

#         for label, color in items:
#             self.canvas.create_rectangle(
#                 x, legend_y - 8, x + box, legend_y + 4, fill=color, width=0
#             )
#             x += box + gap

#             self.canvas.create_text(
#                 x,
#                 legend_y,
#                 text=label,
#                 anchor="w",
#                 fill="#334155",
#                 font=("Segoe UI", 10),
#             )
#             x += 140

# import customtkinter as ctk
# import math


# class AnimatedHorizontalBarChart(ctk.CTkFrame):
#     def __init__(
#         self, master, title="Patient Factors", lines_config=None, bg="#E2E8F0", **kwargs
#     ):
#         super().__init__(master, fg_color="transparent", **kwargs)

#         self.lines_config = lines_config or []
#         self.full_data = []

#         self.chart_container = ctk.CTkFrame(self, fg_color="transparent")
#         self.chart_container.pack(fill="both", expand=True, padx=15, pady=15)

#         self.header_frame = ctk.CTkFrame(self.chart_container, fg_color="transparent")
#         self.header_frame.pack(fill="x", pady=(5, 5))

#         self.title_label = ctk.CTkLabel(
#             self.header_frame,
#             text=title,
#             font=("Inter", 20),
#             text_color="#0F172A",
#         )
#         self.title_label.pack(side="left")

#         self.canvas = ctk.CTkCanvas(self.chart_container, bg=bg, highlightthickness=0)
#         self.canvas.pack(fill="both", expand=True)

#     def update_chart(self, data):
#         self.full_data = data
#         self.draw_chart()

#     def draw_chart(self):
#         self.canvas.delete("all")

#         if not self.full_data:
#             return

#         labels = [d["feature"] for d in self.full_data]
#         values = [d["score"] for d in self.full_data]

#         self.update_idletasks()

#         W = max(self.canvas.winfo_width(), 450)
#         H = max(self.canvas.winfo_height(), 350)

#         left_pad = 140
#         right_pad = 40
#         top_pad = 40
#         bottom_pad = 80

#         chart_width = W - left_pad - right_pad
#         chart_height = H - top_pad - bottom_pad

#         # ===== SCALE FIX =====
#         scale_max = max(abs(v) for v in values) * 1.2 or 1

#         # ===== CENTER LINE =====
#         center_x = left_pad + chart_width / 2

#         self.canvas.create_line(
#             center_x,
#             top_pad,
#             center_x,
#             H - bottom_pad,
#             fill="#94A3B8",
#             dash=(4, 2),
#         )

#         # ===== BAR SETTINGS =====
#         row_height = chart_height / len(values)
#         bar_height = min(18, row_height * 0.5) + 20

#         bars = []

#         for i, label in enumerate(labels):
#             value = values[i]

#             y_center = top_pad + (i * row_height) + row_height / 2
#             y0 = y_center - bar_height / 2
#             y1 = y_center + bar_height / 2

#             color = "#2563EB" if value >= 0 else "#EF4444"

#             rect = self.canvas.create_rectangle(
#                 center_x, y0, center_x, y1, fill=color, width=0
#             )

#             self.canvas.create_text(
#                 20,
#                 y_center,
#                 text=label.replace("_", " ").title(),
#                 anchor="w",
#                 fill="#475569",
#                 font=("Segoe UI", 11),
#             )

#             txt = self.canvas.create_text(
#                 center_x,
#                 y_center,
#                 text="",
#                 anchor="w",
#                 fill="#0F172A",
#                 font=("Segoe UI", 10, "bold"),
#             )

#             bars.append((rect, txt, value, y0, y1))

#         # ===== ANIMATION =====
#         frames = 50
#         duration = 10

#         def animate(frame=0):
#             progress = frame / frames
#             ease = 1 - (1 - progress) ** 3

#             max_bar_width = chart_width * 0.45

#             for rect, txt, value, y0, y1 in bars:
#                 current_val = value * ease

#                 bar_length = (abs(current_val) / scale_max) * max_bar_width

#                 if value >= 0:
#                     x0 = center_x
#                     x1 = center_x + bar_length
#                     text_x = min(x1 + 8, W - right_pad - 20)
#                 else:
#                     x0 = center_x - bar_length
#                     x1 = center_x
#                     text_x = max(x0 - 8, left_pad + 20)

#                 self.canvas.coords(rect, x0, y0, x1, y1)
#                 self.canvas.coords(txt, text_x, (y0 + y1) / 2)

#                 sign = "+" if value >= 0 else "−"
#                 self.canvas.itemconfig(txt, text=f"{sign}{abs(current_val):.2f}")

#             if frame < frames:
#                 self.after(duration, lambda: animate(frame + 1))

#         animate()

#         # ===== X-AXIS TICKS (LIKE SHAP) =====
#         tick_min = 0.15
#         tick_max = 0.55
#         tick_count = 8

#         for i in range(tick_count + 1):
#             ratio = i / tick_count
#             value = tick_min + (tick_max - tick_min) * ratio
#             x = left_pad + ratio * chart_width

#             self.canvas.create_line(
#                 x,
#                 H - bottom_pad + 5,
#                 x,
#                 H - bottom_pad + 10,
#                 fill="#94A3B8",
#             )

#             self.canvas.create_text(
#                 x,
#                 H - bottom_pad + 20,
#                 text=f"{value:.2f}",
#                 fill="#64748B",
#                 font=("Segoe UI", 9),
#             )

#         # ===== LEGEND =====
#         legend_y = H - 10

#         items = [
#             ("Supports Prediction", "#2563EB"),
#             ("Opposes Prediction", "#EF4444"),
#         ]

#         box = 12
#         gap = 6
#         spacing = 40

#         total_width = len(items) * 160
#         x = (W - total_width) / 2

#         for label, color in items:
#             self.canvas.create_rectangle(
#                 x, legend_y - 8, x + box, legend_y + 4, fill=color, width=0
#             )
#             x += box + gap

#             self.canvas.create_text(
#                 x,
#                 legend_y,
#                 text=label,
#                 anchor="w",
#                 fill="#334155",
#                 font=("Segoe UI", 10),
#             )
#             x += 140
import customtkinter as ctk
import math


class AnimatedHorizontalBarChart(ctk.CTkFrame):
    def __init__(
        self, master, title="Patient Factors", lines_config=None, bg="#E2E8F0", **kwargs
    ):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.lines_config = lines_config or []
        self.full_data = []

        self.chart_container = ctk.CTkFrame(self, fg_color="transparent")
        self.chart_container.pack(fill="both", expand=True, padx=15, pady=15)

        self.header_frame = ctk.CTkFrame(self.chart_container, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(5, 5))

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text=title,
            font=("Inter", 18.5),
            text_color="#0F172A",
        )
        self.title_label.pack(side="left")

        self.canvas = ctk.CTkCanvas(self.chart_container, bg=bg, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

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

        W = max(self.canvas.winfo_width(), 450)
        H = max(self.canvas.winfo_height(), 350)

        left_pad = 140
        right_pad = 40
        top_pad = 40
        bottom_pad = 80

        chart_width = W - left_pad - right_pad
        chart_height = H - top_pad - bottom_pad

        # ===== SCALE =====
        scale_max = max(abs(v) for v in values) * 1.2 or 1

        # ===== CENTER LINE =====
        center_x = left_pad + chart_width / 2

        self.canvas.create_line(
            center_x,
            top_pad,
            center_x,
            H - bottom_pad,
            fill="#94A3B8",
            dash=(4, 2),
        )

        # ===== SHAP BASE + FINAL VALUE =====
        base_value = 0.252  # change if you have real base value
        fx_value = base_value + sum(values)

        # ===== BAR SETTINGS =====
        row_height = chart_height / len(values)
        bar_height = min(18, row_height * 0.5) + 20

        bars = []

        for i, label in enumerate(labels):
            value = values[i]

            y_center = top_pad + (i * row_height) + row_height / 2
            y0 = y_center - bar_height / 2
            y1 = y_center + bar_height / 2

            color = "#2563EB" if value >= 0 else "#EF4444"

            rect = self.canvas.create_rectangle(
                center_x, y0, center_x, y1, fill=color, width=0
            )

            self.canvas.create_text(
                20,
                y_center,
                text=label.replace("_", " ").title(),
                anchor="w",
                fill="#475569",
                font=("Segoe UI", 11),
            )

            txt = self.canvas.create_text(
                center_x,
                y_center,
                text="",
                anchor="w",
                fill="#0F172A",
                font=("Segoe UI", 10, "bold"),
            )

            bars.append((rect, txt, value, y0, y1))

        # ===== ANIMATION =====
        frames = 50
        duration = 10

        def animate(frame=0):
            progress = frame / frames
            ease = 1 - (1 - progress) ** 3

            max_bar_width = chart_width * 0.45

            for rect, txt, value, y0, y1 in bars:
                current_val = value * ease

                bar_length = (abs(current_val) / scale_max) * max_bar_width

                if value >= 0:
                    x0 = center_x
                    x1 = center_x + bar_length
                    text_x = min(x1 + 8, W - right_pad - 20)
                else:
                    x0 = center_x - bar_length
                    x1 = center_x
                    text_x = max(x0 - 8, left_pad + 20)

                self.canvas.coords(rect, x0, y0, x1, y1)
                self.canvas.coords(txt, text_x, (y0 + y1) / 2)

                sign = "+" if value >= 0 else "-"
                self.canvas.itemconfig(txt, text=f"{sign}{abs(current_val):.2f}")

            if frame < frames:
                self.after(duration, lambda: animate(frame + 1))

        animate()

        # ===== AUTO X-AXIS TICKS =====
        tick_count = 6

        min_val = min(0, min(values))
        max_val = max(0, max(values))

        padding = (max_val - min_val) * 0.2 or 0.1
        min_val -= padding
        max_val += padding

        for i in range(tick_count + 1):
            ratio = i / tick_count
            val = min_val + (max_val - min_val) * ratio

            x = center_x + (val / scale_max) * (chart_width / 2)

            self.canvas.create_line(
                x,
                H - bottom_pad + 5,
                x,
                H - bottom_pad + 10,
                fill="#94A3B8",
            )

            self.canvas.create_text(
                x,
                H - bottom_pad + 20,
                text=f"{val:.2f}",
                fill="#64748B",
                font=("Segoe UI", 9),
            )

        # ===== SHAP LABELS =====
        self.canvas.create_text(
            left_pad,
            H - 35,
            text=f"E[f(X)] = {base_value:.3f}",
            fill="#64748B",
            font=("Segoe UI", 10),
            anchor="w",
        )

        self.canvas.create_text(
            W - right_pad,
            top_pad - 10,
            text=f"f(x) = {fx_value:.3f}",
            fill="#64748B",
            font=("Segoe UI", 10),
            anchor="e",
        )

        # ===== LEGEND =====
        legend_y = H - 12

        items = [
            ("Supports Prediction", "#2563EB"),
            ("Opposes Prediction", "#EF4444"),
        ]

        box = 12
        gap = 6
        spacing = 30
        font = ("Segoe UI", 10)

        widths = []
        for text, _ in items:
            temp = self.canvas.create_text(0, 0, text=text, font=font, anchor="nw")
            bbox = self.canvas.bbox(temp)
            self.canvas.delete(temp)
            widths.append(bbox[2] - bbox[0])

        total_width = (
            sum(box + gap + widths[i] + spacing for i in range(len(items))) - spacing
        )
        x = (W - total_width) / 2

        for i, (text, color) in enumerate(items):
            self.canvas.create_rectangle(
                x, legend_y - 8, x + box, legend_y + 4, fill=color, width=0
            )
            x += box + gap

            self.canvas.create_text(
                x,
                legend_y,
                text=text,
                anchor="w",
                fill="#334155",
                font=font,
            )
            x += widths[i] + spacing
