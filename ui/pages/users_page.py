import customtkinter as ctk
from PIL import Image
from constants.seeds import (
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    GREEN,
    RED,
    PRIMARY,
    SECONDARY,
    YELLOW,
    VIOLET,
    FUNNEL,
    CROSS,
    PLUS,
    YELLOW_HOVER,
    RED_HOVER,
)

from ..components.create_user_modal import CreateUserModal
from ..components.update_user_modal import UpdateUserModal
from ..components.avatar import Avatar
from ..components.data_table import DataTable
from CTkMessagebox import CTkMessagebox as mb


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
        self.admin_db = controller.admin_db

        self.filter_icon = ctk.CTkImage(Image.open(FUNNEL), size=(30, 30))
        self.plus_icon = ctk.CTkImage(Image.open(PLUS), size=(26, 26))
        self.cross_icon = ctk.CTkImage(Image.open(CROSS), size=(26, 26))

        self.user_filter_frame = ctk.CTkFrame(
            self,
            height=230,
            width=1450,
            fg_color="#E2E8F0",
            corner_radius=20,
        )
        self.user_filter_frame.place(x=0, y=10)
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

        self.add_user_btn = ctk.CTkButton(
            self.user_filter_frame,
            text="Add User",
            font=("Inter", 17, "bold"),
            image=self.plus_icon,
            compound="left",
            height=50,
            width=180,
            fg_color=PRIMARY,
            hover_color=SECONDARY,
            text_color="#FFFFFF",
            corner_radius=9,
            command=self.add_user,
        )
        self.add_user_btn.place(x=1240, y=20)

        ctk.CTkLabel(
            self.user_filter_frame,
            text="Search",
            font=("Poppins", 18),
            text_color="#1E293B",
        ).place(x=31, y=110)

        self.search_entry = ctk.CTkEntry(
            self.user_filter_frame,
            width=500,
            height=50,
            corner_radius=9,
            font=("Inter", 18),
            fg_color="#D3D9E2",
            text_color="#1E293B",
            placeholder_text="Search users...",
            placeholder_text_color="#64748B",
            border_width=0,
        )

        self.delete_search_btn = ctk.CTkButton(
            self.user_filter_frame,
            text="",
            image=self.cross_icon,
            fg_color="#D3D9E2",
            width=0,
            bg_color="#D3D9E2",
            hover=False,
            cursor="hand2",
            command=self.delete_search,
        )
        self.search_entry.place(x=30, y=140)
        self.delete_search_btn.place(x=480, y=148)

        ctk.CTkLabel(
            self.user_filter_frame,
            text="Role",
            font=("Poppins", 18),
            text_color="#1E293B",
        ).place(x=741, y=110)

        self.filter_role_var = ctk.StringVar(value="All")

        self.filter_role_menu = ctk.CTkOptionMenu(
            self.user_filter_frame,
            values=["All", "Patient", "Personnel", "Admin"],
            variable=self.filter_role_var,
            width=230,
            height=50,
            font=("Inter", 18),
            fg_color="#D3D9E2",
            button_color="#CBD5E1",
            button_hover_color="#94A3B8",
            text_color="#1E293B",
            dropdown_fg_color="#FFFFFF",
            dropdown_text_color="#0F172A",
            dropdown_hover_color="#D4D6DA",
            dropdown_font=("Inter", 20),
            corner_radius=9,
            command=lambda value: self.apply_filters(),
        )

        self.filter_role_menu.place(x=740, y=140)
        ctk.CTkLabel(
            self.user_filter_frame,
            text="Status",
            font=("Poppins", 18),
            text_color="#1E293B",
        ).place(x=1191, y=110)
        self.filter_status_var = ctk.StringVar(value="All")

        self.filter_status_menu = ctk.CTkOptionMenu(
            self.user_filter_frame,
            values=["All", "Verified", "Pending"],
            variable=self.filter_status_var,
            width=230,
            height=50,
            font=("Inter", 18),
            fg_color="#D3D9E2",
            button_color="#CBD5E1",
            button_hover_color="#94A3B8",
            text_color="#1E293B",
            dropdown_fg_color="#FFFFFF",
            dropdown_text_color="#0F172A",
            dropdown_hover_color="#D4D6DA",
            dropdown_font=("Inter", 20),
            corner_radius=9,
            # command=self.handle_status_filter,
            command=lambda value: self.apply_filters(),
        )
        self.filter_status_menu.place(x=1190, y=140)

        self.table_container = ctk.CTkFrame(
            self,
            width=1450,
            height=650,
            corner_radius=20,
            fg_color="#E2E8F0",
        )
        self.table_container.place(x=0, y=265)
        self.users_table = ctk.CTkFrame(
            self.table_container,
            fg_color="transparent",
            width=1410,
            height=610,
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
                "hover": YELLOW_HOVER,
                "command": self.update_record,
            },
            {
                "text": "Delete",
                # "icon": self.print_icon,
                "color": RED,
                "hover": RED_HOVER,
                "command": self.delete_record,
            },
        ]
        table_container = ctk.CTkScrollableFrame(
            self.users_table,
            fg_color="#E2E8F0",
            scrollbar_button_color="#6B7280",
            scrollbar_button_hover_color="#4B5563",
        )
        table_container.pack(fill="both", expand=True)
        self.table = DataTable(
            table_container,
            headers=self.table_headers,
            data=self.table_data,
            actions=self.table_actions,
            table_width=232,
            header_color=GREEN,
            row_color="#FFFFFF",
        )

        self.table.pack(
            fill="both",
            expand=True,
        )
        self.search_entry.bind("<KeyRelease>", lambda e: self.apply_filters())

    def apply_filters(self):
        keyword = self.search_entry.get().strip()
        role = self.filter_role_var.get()
        status = self.filter_status_var.get()

        records = self.admin_db.filter_users(keyword, role, status)
        records = records or []

        self.full_records = records

        if records:
            table_data = [r.get("display", ("-", "-", "-", "-", "-")) for r in records]
        else:
            table_data = [("No Results", "-", "-", "-", "-", "-")]

        self.table.update_data(table_data)

    def delete_search(self):
        self.search_entry.delete(0, ctk.END)
        self.on_show()

    def clear_fields(self):
        self.search_entry.delete(0, ctk.END)
        self.filter_role_var.set("All")
        self.filter_status_var.set("All")

    def on_show(self):

        self.user_records = self.admin_db.fetch_all_users()

        if self.user_records:
            table_data = [r["display"] for r in self.user_records]
        else:
            table_data = [("No Results", "-", "-", "-", "-", "-")]

        self.table.update_data(table_data)

    def add_user(self):
        x = self.user_filter_frame.winfo_rootx()
        y = self.user_filter_frame.winfo_rooty()

        self.top = CreateUserModal(
            self,
            controller=self.controller,
            x=x,
            y=y,
        )
        self.top.transient(self)

        self.top.title("LeptoSight")
        self.top.geometry(f"1030x590+{x}+{y}")

    def update_record(self, index):
        x = self.user_filter_frame.winfo_rootx()
        y = self.user_filter_frame.winfo_rooty()
        record = self.user_records[index]

        self.top = UpdateUserModal(
            self,
            row=record["full"],
            controller=self.controller,
            x=x,
            y=y,
        )
        self.top.transient(self)

        self.top.title("LeptoSight")
        self.top.geometry(f"1030x790+{x}+{y}")

    def delete_record(self, index):
        record = self.user_records[index]
        user_id = record["id"]

        confirm = mb(
            self,
            title="Delete User",
            message="Are you sure you want to delete this user?",
            icon="warning",
            option_1="Delete",
            option_2="Cancel",
            fg_color="#FFFFFF",
            border_width=1,
            border_color="#E2E8F0",
            text_color="#0F172A",
            title_color="#0F172A",
            font=("Inter", 16),
            height=260,
            button_color=RED,
            button_hover_color=RED_HOVER,
            button_text_color="#FFFFFF",
            button_width=100,
            button_height=55,
        )

        # 🔥 IMPORTANT: get response
        if confirm.get() != "Delete":
            return

        # ✅ CALL SERVICE
        result = self.admin_db.delete_user(user_id)

        if result == "USER_DELETED":
            self.on_show()

        elif result == "USER_NOT_FOUND":

            mb(
                self,
                title="Error",
                message="User not found",
                options=("Okay",),
                icon="cancel",
            )

        else:
            mb(
                self,
                title="Error",
                message="Delete failed",
                options=("Okay",),
                icon="cancel",
            )
