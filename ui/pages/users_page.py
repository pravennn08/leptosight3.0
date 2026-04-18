import customtkinter as ctk
from PIL import Image
from constants.seeds import (
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    GREEN,
    CAMERA,
    FLASH,
    SAVE,
    CHECK,
    BLUE,
    RED,
    EYE,
    LOGO,
    DISTANCE,
    PRIMARY,
    CAMERA_TIPS,
    CAMERA_PROMPT,
    RECOMMENDATIONS,
    SECONDARY,
    QUESTIONS,
    CHEVRON_LEFT,
    CHEVRON_RIGHT,
    YELLOW,
    FILTER,
    VIOLET,
    FUNNEL,
    CROSS,
    PLUS,
)
from ..components.avatar import Avatar
from ..components.data_table import DataTable
from ..components.avatar import Avatar
from ..components.square import Square
from ..components.rectangle import Rectangle


class UsersPage(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(
            master,
            # fg_color="#F8FAFC",
            # border_width=1,
            # border_color="#E2E8F0",
            fg_color="transparent",
        )
        self.controller = controller

        self.filter_icon = ctk.CTkImage(Image.open(FUNNEL), size=(30, 30))
        self.plus_icon = ctk.CTkImage(Image.open(PLUS), size=(26, 26))
        self.cross_icon = ctk.CTkImage(Image.open(CROSS), size=(26, 26))

        ctk.CTkLabel(
            self, text="Users", font=("Arial", 33, "bold"), text_color=TEXT_PRIMARY
        ).place(x=40, y=10)
        # ctk.CTkLabel(
        #     self,
        #     text="Manage user accounts, roles, and account status efficiently.",
        #     font=("Poppins", 20),
        #     text_color=TEXT_SECONDARY,
        # ).place(x=40, y=60)

        self.user_filter_frame = ctk.CTkFrame(
            self,
            height=230,
            width=1400,
            fg_color="#E2E8F0",
            corner_radius=20,
        )
        self.user_filter_frame.place(x=40, y=70)
        Avatar(
            self.user_filter_frame,
            width=60,
            height=60,
            image=self.filter_icon,
            fg_color=VIOLET,
        ).place(x=30, y=20)
        ctk.CTkLabel(
            self.user_filter_frame,
            text=" User Filters",
            font=("Poppins", 22, "bold"),
            # text_color=TEXT_PRIMARY,
            text_color="#1E293B",
        ).place(x=100, y=30)

        ctk.CTkButton(
            self.user_filter_frame,
            text="Add User",
            font=("Inter", 19, "bold"),
            image=self.plus_icon,
            compound="left",
            height=50,
            width=180,
            fg_color=PRIMARY,
            hover_color=SECONDARY,
            text_color="#FFFFFF",
            corner_radius=9,
        ).place(x=1190, y=20)

        ctk.CTkLabel(
            self.user_filter_frame,
            text="Search",
            font=("Poppins", 18),
            text_color=TEXT_SECONDARY,
        ).place(x=31, y=110)

        self.search_entry = ctk.CTkEntry(
            self.user_filter_frame,
            width=500,
            height=45,
            corner_radius=9,
            font=("Roboto", 18),
            fg_color="#D3D9E2",
            text_color="#1E293B",
            placeholder_text="Search users...",
            placeholder_text_color="#64748B",
            border_width=0,
        )

        self.delete_search = ctk.CTkButton(
            self.user_filter_frame,
            text="",
            image=self.cross_icon,
            fg_color="#D3D9E2",
            width=0,
            bg_color="#D3D9E2",
            hover=False,
            cursor="hand2",
        )
        self.search_entry.place(x=30, y=140)
        self.delete_search.place(x=485, y=145)

        ctk.CTkLabel(
            self.user_filter_frame,
            text="Role",
            font=("Poppins", 18),
            text_color=TEXT_SECONDARY,
        ).place(x=721, y=110)

        self.filter_role_var = ctk.StringVar(value="All")

        self.filter_role_menu = ctk.CTkOptionMenu(
            self.user_filter_frame,
            values=["All", "Patient", "Personnel", "Admin"],
            variable=self.filter_role_var,
            width=230,
            height=45,
            font=("Inter", 18),
            fg_color="#D3D9E2",  # match search bar
            button_color="#CBD5E1",  # subtle gray-blue
            button_hover_color="#94A3B8",  # darker on hover
            text_color="#1E293B",  # dark readable text
            dropdown_fg_color="#FFFFFF",
            dropdown_text_color="#0F172A",
            dropdown_hover_color="#D4D6DA",
            dropdown_font=("Inter", 20),
            corner_radius=9,
        )

        self.filter_role_menu.place(x=720, y=140)
        ctk.CTkLabel(
            self.user_filter_frame,
            text="Status",
            font=("Poppins", 18),
            text_color=TEXT_SECONDARY,
        ).place(x=1141, y=110)
        self.filter_status_var = ctk.StringVar(value="All")

        self.filter_status_menu = ctk.CTkOptionMenu(
            self.user_filter_frame,
            values=["All", "Verified", "Pending"],
            variable=self.filter_status_var,
            width=230,
            height=45,
            font=("Inter", 18),
            fg_color="#D3D9E2",  # match search bar
            button_color="#CBD5E1",  # subtle gray-blue
            button_hover_color="#94A3B8",  # darker on hover
            text_color="#1E293B",  # dark readable text
            dropdown_fg_color="#FFFFFF",
            dropdown_text_color="#0F172A",
            dropdown_hover_color="#D4D6DA",
            dropdown_font=("Inter", 20),
            corner_radius=9,
        )
        self.filter_status_menu.place(x=1140, y=140)

        self.table_container = ctk.CTkFrame(
            self,
            width=1400,
            height=590,
            corner_radius=20,
            fg_color="#E2E8F0",
        )
        self.table_container.place(x=40, y=325)
        self.users_table = ctk.CTkFrame(
            self.table_container,
            fg_color="transparent",
            width=1350,
            height=550,
        )

        self.users_table.pack(fill="both", expand=True, padx=20, pady=20)
        self.users_table.pack_propagate(False)

        self.table_headers = [
            "User ID",
            "Email",
            "Phone Number",
            "Role",
            "Status",
            "Actions",
        ]
        self.table_data = []
        self.table_actions = [
            {
                "text": "Update",
                # "icon": self.view_icon,
                "color": YELLOW,
                # "hover": "#2563EB",
                "command": self.update_record,
            },
            {
                "text": "Delete",
                # "icon": self.print_icon,
                "color": RED,
                # "hover": "#B91C1C",
                "command": self.delete_record,
            },
        ]
        table_container = ctk.CTkScrollableFrame(
            self.users_table,
            fg_color="#E2E8F0",
            scrollbar_button_color="#6B7280",
            scrollbar_button_hover_color="#4B5563",
        )
        table_container.pack(fill="both", expand=True, pady=(10))
        self.table = DataTable(
            table_container,
            headers=self.table_headers,
            data=self.table_data,
            actions=self.table_actions,
            table_width=220,
            header_color=GREEN,
            row_color="#FFFFFF",
        )

        self.table.pack(
            fill="both",
            expand=True,
        )

    def on_show(self):

        self.user_records = self.controller.db.fetch_all_users()

        if self.user_records:
            table_data = [r["display"] for r in self.user_records]
        else:
            table_data = [("No Results", "-", "-", "-", "-", "-")]

        self.table.update_data(table_data)

    def update_record(self, index):
        x = self.user_filter_frame.winfo_rootx()
        y = self.user_filter_frame.winfo_rooty()
        record = self.user_records[index]

        self.top = UpdateUserModal(
            self,
            row=record["full"],
            x=x,
            y=y,
        )

        self.top.title("LeptoSight")
        self.top.geometry(f"1030x790+{x}+{y}")
        self.top.transient(self)

    def delete_record(self, index):
        pass


class UpdateUserModal(ctk.CTkToplevel):
    def __init__(self, master, row=None, x=100, y=100, *args, **kwargs):
        super().__init__(master, fg_color="#FFFFFF", *args, **kwargs)

        self.row = row
        self.pos_x = x
        self.pos_y = y

        self.eye_icon = ctk.CTkImage(Image.open(EYE), size=(35, 35))
        # self.percent_icon = ctk.CTkImage(Image.open(PERCENT), size=(35, 35))

        self.after(50, self.set_position)
        self.after(100, self.safe_grab)
        # SYSTEM LOGO
        self.logo_img = ctk.CTkImage(
            light_image=Image.open(LOGO),
            size=(51, 51),
        )

        self.container = ctk.CTkFrame(
            self,
            width=990,
            height=760,
            # fg_color="#E2E8F0",
            fg_color="transparent",
        )
        self.container.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        Square(
            self.container,
            size=60,
            image=self.logo_img,
            fg_color=PRIMARY,
        ).place(x=10, y=0)
        ctk.CTkLabel(
            self.container,
            text="LeptoSight",
            font=("Inter", 22, "bold"),
            text_color=TEXT_PRIMARY,
        ).place(x=90, y=5)

        ctk.CTkLabel(
            self.container,
            text="An AI-Powered for Early Detection of Leptospirosis",
            font=("Inter", 16),
            wraplength=670,
            justify="left",
            text_color=TEXT_SECONDARY,
        ).place(x=90, y=30)

        ctk.CTkLabel(
            self.container,
            text="Update Record",
            font=("Inter", 22, "bold"),
            text_color="#1E293B",
        ).place(x=10, y=90)

        self.id_badge = Rectangle(
            self.container,
            width=130,
            height=40,
            corner_radius=8,
            text="User ID: N/A",
            fg_color="#8B5CF6",
            text_color="#FFFFFF",
            font=("Inter", 15, "bold"),
        )
        self.id_badge.place(x=850, y=70)

        ctk.CTkLabel(
            self.container,
            text="Full Name",
            font=("Poppins", 17),
            text_color=TEXT_SECONDARY,
        ).place(x=11, y=140)

        self.full_name_entry = ctk.CTkEntry(
            self.container,
            width=400,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            text_color="#1E293B",  # dark readable text
            fg_color="#E2E8F0",
            border_width=0,
        )
        self.full_name_entry.place(x=10, y=180)

        ctk.CTkLabel(
            self.container,
            text="Email",
            font=("Poppins", 17),
            text_color=TEXT_SECONDARY,
        ).place(x=581, y=140)

        self.email_entry = ctk.CTkEntry(
            self.container,
            width=400,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            border_width=0,
            fg_color="#E2E8F0",
            text_color="#1E293B",  # dark readable text
        )
        self.email_entry.place(x=580, y=180)

        ctk.CTkLabel(
            self.container,
            text="Phone Number",
            font=("Poppins", 17),
            text_color=TEXT_SECONDARY,
        ).place(x=11, y=240)

        self.phone_number_entry = ctk.CTkEntry(
            self.container,
            width=400,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            text_color="#1E293B",  # dark readable text
            fg_color="#E2E8F0",
            border_width=0,
        )
        self.phone_number_entry.place(x=10, y=280)

        ctk.CTkLabel(
            self.container,
            text="Role",
            font=("Poppins", 17),
            text_color=TEXT_SECONDARY,
        ).place(x=581, y=240)

        self.roles = ctk.StringVar(value="Patient")
        self.role_option_menu = ctk.CTkOptionMenu(
            self.container,
            values=["Patient", "Personnel", "Admin"],
            variable=self.roles,
            width=400,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            fg_color="#E2E8F0",
            button_color="#CBD5E1",
            button_hover_color="#94A3B8",
            text_color="#1E293B",
            dropdown_fg_color="#FFFFFF",
            dropdown_text_color="#0F172A",
            dropdown_hover_color="#D4D6DA",
            dropdown_font=("Roboto", 19),
        )
        self.role_option_menu.place(x=580, y=280)

        ctk.CTkLabel(
            self.container,
            text="Password",
            font=("Poppins", 17),
            text_color=TEXT_SECONDARY,
        ).place(x=11, y=340)

        self.password_entry = ctk.CTkEntry(
            self.container,
            width=400,
            height=50,
            corner_radius=9,
            font=("Roboto", 17),
            text_color="#1E293B",
            fg_color="#E2E8F0",
            border_width=0,
        )
        self.password_entry.place(x=10, y=380)

        ctk.CTkLabel(
            self.container,
            text="Status",
            font=("Poppins", 17),
            text_color=TEXT_SECONDARY,
        ).place(x=581, y=340)

        self.status = ctk.StringVar(value="Verified")
        self.status_option_menu = ctk.CTkOptionMenu(
            self.container,
            values=["Verified", "Pending"],
            variable=self.status,
            width=400,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            fg_color="#E2E8F0",
            button_color="#CBD5E1",
            button_hover_color="#94A3B8",
            text_color="#1E293B",
            dropdown_fg_color="#FFFFFF",
            dropdown_text_color="#0F172A",
            dropdown_hover_color="#D4D6DA",
            dropdown_font=("Roboto", 19),
        )
        self.status_option_menu.place(x=580, y=380)

        ctk.CTkLabel(
            self.container,
            text="Last Login",
            font=("Poppins", 17),
            text_color=TEXT_SECONDARY,
        ).place(x=11, y=440)

        self.last_login_entry = ctk.CTkEntry(
            self.container,
            width=400,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            text_color="#1E293B",  # dark readable text
            fg_color="#E2E8F0",
            border_width=0,
        )
        self.last_login_entry.place(x=10, y=480)

        ctk.CTkLabel(
            self.container,
            text="Created At",
            font=("Poppins", 17),
            text_color=TEXT_SECONDARY,
        ).place(x=581, y=440)

        self.created_entry = ctk.CTkEntry(
            self.container,
            width=400,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            text_color="#1E293B",  # dark readable text
            fg_color="#E2E8F0",
            border_width=0,
        )
        self.created_entry.place(x=580, y=480)

        ctk.CTkLabel(
            self.container,
            text="Updated At",
            font=("Poppins", 17),
            text_color=TEXT_SECONDARY,
        ).place(x=11, y=540)

        self.updated_entry = ctk.CTkEntry(
            self.container,
            width=400,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            text_color="#1E293B",  # dark readable text
            fg_color="#E2E8F0",
            border_width=0,
        )
        self.updated_entry.place(x=10, y=580)

        self.update_button = ctk.CTkButton(
            self.container,
            width=150,
            height=50,
            text="Save",
            fg_color="#14B8A6",
            hover_color="#0D9488",
            text_color="#FFFFFF",
            font=("Inter", 18, "bold"),
            command=lambda: self.destroy(),
            corner_radius=9,
        )
        self.update_button.place(x=830, y=690)

        ctk.CTkButton(
            self.container,
            width=150,
            height=50,
            text="Close",
            fg_color="#E2E8F0",
            hover_color="#CBD5E1",
            text_color="#1E293B",
            font=("Inter", 18, "bold"),
            corner_radius=9,
            command=lambda: self.destroy(),
        ).place(x=650, y=690)
        self.populate_data()

    def populate_data(self):
        from datetime import datetime

        data = self.row
        user_id = data.get("id")
        self.id_badge.set_text(f"User ID: {user_id}")

        self.full_name_entry.delete(0, "end")
        self.full_name_entry.insert(0, data.get("name") or "")

        self.email_entry.delete(0, "end")
        self.email_entry.insert(0, data.get("email") or "")

        self.phone_number_entry.delete(0, "end")
        self.phone_number_entry.insert(0, data.get("phone_number"))

        self.password_entry.insert(0, data.get("password"))
        self.password_entry.configure(state="disabled", show="*")

        role = data.get("role")
        self.role_option_menu.set(role.capitalize() if role else "Patient")

        verified = data.get("is_verified")
        is_verified = str(verified).lower() in ("true", "1", "t")
        self.status_option_menu.set("Verified" if is_verified else "Pending")

        self.created_entry.delete(0, "end")
        self.created_entry.insert(0, self.format_datetime(data.get("created_at")))
        self.created_entry.configure(state="disabled")

        self.updated_entry.delete(0, "end")
        self.updated_entry.insert(0, self.format_datetime(data.get("updated_at")))
        self.updated_entry.configure(state="disabled")

        self.last_login_entry.delete(0, "end")
        self.last_login_entry.insert(0, self.format_datetime(data.get("last_login_at")))
        self.last_login_entry.configure(state="disabled")

    def format_datetime(self, value):
        from datetime import datetime

        if not value:
            return "N/A"

        try:
            if isinstance(value, str):
                value = datetime.fromisoformat(value)

            return value.strftime("%b %d, %Y | %I:%M %p")
        except:
            return str(value)

    def update_account(self):
        pass

    def set_position(self):
        width = 1030
        height = 790
        self.geometry(f"{width}x{height}+{self.pos_x +200}+{self.pos_y+30}")

    def safe_grab(self):
        try:
            self.grab_set()
        except:
            pass

    def close(self):
        try:
            self.grab_release()
        except:
            pass
        self.destroy()
