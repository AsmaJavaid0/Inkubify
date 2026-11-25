import re
from datetime import date
from urllib.parse import urlparse

USERNAME_REGEX = re.compile(r"^[a-z][a-z0-9_]{2,19}$")
FULL_NAME_REGEX = re.compile(r"^[A-Za-zÀ-ÖØ-öø-ÿ .'-]+$")
INSTAGRAM_HANDLE_REGEX = re.compile(r"^[A-Za-z0-9._]{1,30}$")
CITY_REGEX = re.compile(r"^[A-Za-z0-9 .'-]{2,60}$")

RESERVED_USERNAMES: frozenset[str] = frozenset(
    {
        "admin",
        "administrator",
        "api",
        "app",
        "auth",
        "billing",
        "business",
        "confirm",
        "contact",
        "dashboard",
        "docs",
        "founder",
        "health",
        "help",
        "info",
        "inkubify",
        "login",
        "logout",
        "me",
        "mod",
        "moderator",
        "null",
        "official",
        "onboarding",
        "privacy",
        "profile",
        "profiles",
        "reset",
        "root",
        "security",
        "settings",
        "signup",
        "staff",
        "support",
        "system",
        "team",
        "terms",
        "undefined",
        "user",
        "users",
        "verify",
        "welcome",
        "www",
    }
)

PROVINCE_CITIES: dict[str, tuple[str, ...]] = {
    "Punjab": (
        "Lahore",
        "Faisalabad",
        "Rawalpindi",
        "Multan",
        "Gujranwala",
        "Sialkot",
        "Bahawalpur",
        "Sargodha",
        "Sheikhupura",
        "Rahim Yar Khan",
        "Jhang",
        "Dera Ghazi Khan",
        "Gujrat",
        "Sahiwal",
        "Wah Cantonment",
        "Kasur",
        "Okara",
        "Chiniot",
        "Kamoke",
        "Hafizabad",
    ),
    "Sindh": (
        "Karachi",
        "Hyderabad",
        "Sukkur",
        "Larkana",
        "Nawabshah",
        "Mirpur Khas",
        "Jacobabad",
        "Shikarpur",
        "Khairpur",
        "Dadu",
        "Tando Adam",
        "Thatta",
        "Badin",
    ),
    "Khyber Pakhtunkhwa": (
        "Peshawar",
        "Mardan",
        "Mingora",
        "Kohat",
        "Abbottabad",
        "Dera Ismail Khan",
        "Nowshera",
        "Charsadda",
        "Swabi",
        "Mansehra",
        "Haripur",
        "Bannu",
        "Chitral",
    ),
    "Balochistan": (
        "Quetta",
        "Turbat",
        "Khuzdar",
        "Hub",
        "Chaman",
        "Gwadar",
        "Sibi",
        "Zhob",
        "Loralai",
        "Dera Murad Jamali",
    ),
    "Islamabad Capital Territory": ("Islamabad",),
    "Gilgit-Baltistan": (
        "Gilgit",
        "Skardu",
        "Chilas",
        "Hunza",
        "Ghizer",
        "Astore",
        "Khaplu",
    ),
    "Azad Jammu & Kashmir": (
        "Muzaffarabad",
        "Mirpur",
        "Rawalakot",
        "Kotli",
        "Bhimber",
        "Bagh",
        "Pallandri",
    ),
}

ALL_KNOWN_CITIES_TO_PROVINCES: dict[str, set[str]] = {}
for _prov, _cities in PROVINCE_CITIES.items():
    for _c in _cities:
        ALL_KNOWN_CITIES_TO_PROVINCES.setdefault(_c.lower(), set()).add(_prov)


def normalize_username(raw: str) -> str:
    cleaned = raw.strip().lower()
    if not USERNAME_REGEX.match(cleaned):
        raise ValueError(
            "Username must be 3-20 characters, start with a letter, "
            "and use lowercase letters, numbers, or underscores"
        )
    if cleaned in RESERVED_USERNAMES:
        raise ValueError("This username is reserved")
    return cleaned


def normalize_full_name(raw: str) -> str:
    collapsed = re.sub(r"\s+", " ", raw.strip())
    if not (2 <= len(collapsed) <= 60):
        raise ValueError("Full name must be between 2 and 60 characters")
    if not FULL_NAME_REGEX.match(collapsed):
        raise ValueError(
            "Full name may only contain letters, spaces, periods, apostrophes, and hyphens"
        )
    return collapsed


def validate_date_of_birth(dob: date) -> date:
    today = date.today()
    if dob < date(1930, 1, 1):
        raise ValueError("Date of birth cannot be before 1930")
    if dob > today:
        raise ValueError("Date of birth cannot be in the future")
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    if age < 18:
        raise ValueError("You must be at least 18 years old")
    return dob


def validate_province_and_city(
    province: str | None, city: str | None
) -> tuple[str | None, str | None]:
    if province is not None and province not in PROVINCE_CITIES:
        raise ValueError("Please select a valid province or territory in Pakistan")

    if city is not None:
        cleaned_city = re.sub(r"\s+", " ", city.strip())
        if cleaned_city.lower() == "other":
            raise ValueError("Please enter your city name")
        if not CITY_REGEX.match(cleaned_city):
            raise ValueError("City must be 2-60 valid characters")
        if province is not None:
            known_provinces = ALL_KNOWN_CITIES_TO_PROVINCES.get(cleaned_city.lower())
            if known_provinces is not None and province not in known_provinces:
                raise ValueError(f"{cleaned_city} does not belong to {province}")
        city = cleaned_city

    return province, city


def normalize_instagram_url(raw: str | None) -> str | None:
    if raw is None:
        return None
    val = raw.strip()
    if not val:
        return None

    if val.startswith("@"):
        handle = val[1:].strip("/")
    elif "instagram.com" in val.lower():
        if not val.lower().startswith(("http://", "https://")):
            val = f"https://{val}"
        parsed = urlparse(val)
        host = (parsed.hostname or "").lower()
        if host not in ("instagram.com", "www.instagram.com"):
            raise ValueError("Instagram link must point to instagram.com")
        path_parts = [p for p in parsed.path.split("/") if p]
        if not path_parts:
            raise ValueError("Please provide a valid Instagram handle or profile URL")
        handle = path_parts[0].lstrip("@")
    else:
        handle = val.strip("/")

    if not INSTAGRAM_HANDLE_REGEX.match(handle):
        raise ValueError("Invalid Instagram handle or URL")
    return f"https://instagram.com/{handle}"


def validate_linkedin_url(raw: str | None) -> str | None:
    if raw is None:
        return None
    val = raw.strip()
    if not val:
        return None

    if not val.lower().startswith(("http://", "https://")):
        val = f"https://{val}"
    parsed = urlparse(val)
    host = (parsed.hostname or "").lower()
    if host != "linkedin.com" and not host.endswith(".linkedin.com"):
        raise ValueError("LinkedIn URL must be on linkedin.com")
    if not parsed.path or parsed.path == "/":
        raise ValueError("Please enter your full LinkedIn profile URL")
    return val
