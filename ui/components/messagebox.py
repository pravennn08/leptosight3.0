from CTkMessagebox import CTkMessagebox


class MessageBox:
    def __init__(
        self,
        title="Message",
        message="",
        options=("OK",),
        icon="info",
    ):
        self.title = title
        self.message = message
        self.options = options
        self.icon = icon

    def show(self):
        # 🔥 Build dynamic options
        option_kwargs = {}

        if len(self.options) >= 1:
            option_kwargs["option_1"] = self.options[0]
        if len(self.options) >= 2:
            option_kwargs["option_2"] = self.options[1]
        if len(self.options) >= 3:
            option_kwargs["option_3"] = self.options[2]

        msg = CTkMessagebox(
            title=self.title,
            message=self.message,
            # STYLE
            fg_color="#FFFFFF",
            border_width=1,
            border_color="#E2E8F0",
            text_color="#0F172A",
            title_color="#0F172A",
            font=("Inter", 16),
            # BUTTON
            button_color="#14B8A6",
            button_hover_color="#0D9488",
            button_text_color="#FFFFFF",
            button_width=100,
            button_height=50,
            # CLOSE
            cancel_button="cross",
            cancel_button_color="transparent",
            # BEHAVIOR
            sound=True,
            fade_in_duration=150,
            icon=self.icon,
            **option_kwargs
        )

        return msg.get()
