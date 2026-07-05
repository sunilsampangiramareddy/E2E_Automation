import imaplib
import email
import re
import requests


class ReadOTP:
    # Static config based on your values
    USER_EMAIL = "AutoUser@netapp.com"
    PORT = 993
    PROTOCOL = "imaps"
    EXPECTED_SUBJECT = "OTP Email"
    MAX_MAILS = 1000
    FOLDER_PATH = "INBOX"
    HOST = "outlook.office365.com"
    CLIENT_ID = "6fa4d0e2-51be-48ca-b4fb-4468697ff292"
    CLIENT_SECRET = "a1Y8Q~jm18mO1T1Lc~f5~9TYIrs0b2ioovfRWaOg"
    TOKEN_URL = "https://login.microsoftonline.com/4b0911a0-929b-4715-944b-c03745165b3a/oauth2/v2.0/token"

    @classmethod
    def _get_access_token(cls) -> str:
        payload = {
            "client_id": cls.CLIENT_ID,
            "client_secret": cls.CLIENT_SECRET,
            "grant_type": "client_credentials",
            "scope": "https://outlook.office365.com/.default",
        }
        resp = requests.post(cls.TOKEN_URL, data=payload)
        resp.raise_for_status()
        token_data = resp.json()
        return token_data["access_token"]

    @classmethod
    def _connect_imap(cls, access_token: str):
        mail = imaplib.IMAP4_SSL(cls.HOST, cls.PORT)
        auth_string = f"user={cls.USER_EMAIL}\1auth=Bearer {access_token}\1\1"
        mail.authenticate("XOAUTH2", lambda x: auth_string)
        mail.select(cls.FOLDER_PATH)
        return mail

    @classmethod
    def get_otp_from_imap(cls) -> str | None:
        """Connect via OAuth2 IMAP and return the OTP email body (or None)."""
        access_token = cls._get_access_token()
        mail = cls._connect_imap(access_token)

        try:
            status, data = mail.search(None, "ALL")
            if status != "OK":
                return None

            email_ids = data[0].split()[-cls.MAX_MAILS :]  # latest up to MAX_MAILS

            for email_id in reversed(email_ids):  # start from latest
                status, msg_data = mail.fetch(email_id, "(RFC822)")
                if status != "OK":
                    continue

                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)

                subject = msg.get("subject", "")
                if cls.EXPECTED_SUBJECT not in subject:
                    continue

                if msg.is_multipart():
                    body = ""
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode(errors="ignore")
                            break
                else:
                    body = msg.get_payload(decode=True).decode(errors="ignore")

                # Extract OTP using regex
                otp_match = re.search(r"\b\d{6}\b", body)
                if otp_match:
                    otp = otp_match.group(0)
                    print(f"Extracted OTP: {otp}")  # Debugging OTP
                    return otp

            return None
        finally:
            try:
                mail.logout()
            except Exception:
                pass
