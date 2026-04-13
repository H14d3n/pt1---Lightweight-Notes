import csv
import io
import os
import platform
from cryptography.fernet import Fernet, InvalidToken
from encryption import hash_password


FIELDNAMES = ["uid", "first_name", "password"]
CREDENTIAL_PREFIX = "cred$fernet$v1|"

def determine_windows():
    """Determine if the operating system is Windows."""
    return platform.system() == "Windows"


def get_base_path():
    """Returns the application data directory path based on the operating system."""
    if determine_windows():
        base_path = os.path.join(os.getenv('APPDATA'), "pt1_Lightweight_Notes")
    else:
        base_path = os.path.join(os.path.expanduser("~"), ".config", "pt1_Lightweight_Notes")

    os.makedirs(base_path, exist_ok=True)
    return base_path

def get_csv_path():
    """Returns the path to the CSV file based on the operating system."""
    return os.path.join(get_base_path(), "login.csv")


def get_credentials_key_path():
    """Returns the key file path used for credential-store encryption."""
    return os.path.join(get_base_path(), "credentials.key")


def _get_fernet():
    key_path = get_credentials_key_path()
    if not os.path.exists(key_path):
        key = Fernet.generate_key()
        with open(key_path, mode='wb') as key_file:
            key_file.write(key)
    else:
        with open(key_path, mode='rb') as key_file:
            key = key_file.read().strip()

    return Fernet(key)


def _serialize_rows(rows):
    stream = io.StringIO()
    writer = csv.DictWriter(stream, fieldnames=FIELDNAMES, delimiter=';')
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()


def _deserialize_rows(csv_text):
    stream = io.StringIO(csv_text)
    reader = csv.DictReader(stream, delimiter=';')
    rows = []
    for row in reader:
        rows.append(
            {
                "uid": row.get("uid", ""),
                "first_name": row.get("first_name", ""),
                "password": row.get("password", ""),
            }
        )
    return rows


def write_credentials_rows(rows):
    """Encrypt and persist credential rows to the login store."""
    csv_text = _serialize_rows(rows)
    token = _get_fernet().encrypt(csv_text.encode('utf-8')).decode('ascii')
    payload = f"{CREDENTIAL_PREFIX}{token}"

    with open(csv_file_path, mode='w', encoding='utf-8', newline='') as file:
        file.write(payload)


def read_credentials_rows():
    """Read credential rows, transparently migrating legacy plaintext CSV to encrypted storage."""
    if not check_csv_exists():
        return []

    with open(csv_file_path, mode='r', encoding='utf-8', newline='') as file:
        raw = file.read().strip()

    if not raw:
        return []

    if raw.startswith(CREDENTIAL_PREFIX):
        token = raw[len(CREDENTIAL_PREFIX):]
        try:
            csv_text = _get_fernet().decrypt(token.encode('ascii')).decode('utf-8')
        except InvalidToken as exc:
            raise ValueError("Credential store could not be decrypted.") from exc
        return _deserialize_rows(csv_text)

    # Legacy plaintext CSV migration path.
    rows = _deserialize_rows(raw)
    write_credentials_rows(rows)
    return rows

# Define the CSV file path
csv_file_path = get_csv_path()

def check_csv_exists():
    """Check if the CSV file exists."""
    return os.path.exists(csv_file_path)

def create_csv():
    """Creates the CSV file with a header if it doesn't exist."""
    if check_csv_exists():
        # Also triggers migration if the file is still plaintext CSV.
        read_credentials_rows()
        print(f"Credential store already exists at {csv_file_path}")
        return

    default_rows = [{"uid": "1", "first_name": "admin", "password": hash_password("localadminfern")}]
    write_credentials_rows(default_rows)
    print(f"Encrypted credential store created at {csv_file_path}")