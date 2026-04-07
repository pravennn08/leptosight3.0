class User:
    ADMIN = "admin"
    PERSONNEL = "personnel"
    PATIENT = "patient"

    ROLES = [ADMIN, PERSONNEL, PATIENT]

    def __init__(
        self,
        name,
        email,
        phone_number,
        password,
        otp_code=None,
        otp_expires_at=None,
        role=PATIENT,
        is_verified=False,
        last_login_at=None,
        last_otp_verified_at=None,
    ):
        self.name = name
        self.email = email
        self.phone_number = User.normalize_phone(phone_number)

        self.password = password

        self.otp_code = str(otp_code) if otp_code is not None else None
        self.otp_expires_at = otp_expires_at

        self.role = role if role in self.ROLES else self.PATIENT

        self.is_verified = is_verified
        self.last_login_at = last_login_at
        self.last_otp_verified_at = last_otp_verified_at

    @staticmethod
    def normalize_phone(phone):
        phone = str(phone).strip()

        if phone.startswith("09"):
            return "+63" + phone[1:]
        if phone.startswith("639"):
            return "+" + phone
        return phone
