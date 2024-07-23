import re
from tkinter.constants import NO

def hasEmail(data: dict):
    if data['Email']:
        return True
    else:
        return False

def hasPhone(data: dict):
    if data['Phone'] or data['Mobile']:
        return True
    else:
        return False

def isPhoneValidFormat(phone: str):
    from src.normalization import Norm_Phone
    phone = Norm_Phone(phone)

    if phone.isnumeric():
        if len(phone) <= 4 or len(phone) >= 15:
            return False
        return True
    else:
        return False 

def isEmailValidFormat(email:str):
    from src.normalization import Norm_Email
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email = Norm_Email(email)
    if re.fullmatch(regex, email):
        return True
    else:
        return False
    
def check_OPTIN(s: str):
    s = s.lower().strip()
    s = s = re.sub(r"\s+", "", s)

    if s == 'no':
        return True
    else:
        return False

def check_OPTOUT(s: str):
    s = s.lower().strip()
    s = s = re.sub(r"\s+", "", s)
    
    if s == 'no':
        return False
    else:
        return True
    
def staffMail():
    return [
        "adimahkota.com",
        "balifreestay.com",
        "baligetaway",
        "discoverkarma",
        "discoveryourkarma",
        "haathimahal.com",
        "karmaapsara.com",
        "karmabahamas.com",
        "karmabavaria.com",
        "karmabeach.com",
        "karmaborgodicolleoli.com",
        "karmacamino.com",
        "karmaclub.com",
        "karmaclub.community",
        "karmaclubhouse",
        "karmaconcierge",
        "karma-concierge",
        "karmaconstellation.com",
        "karmadestinations.com",
        "karmadevelopments.com",
        "karmaestates.com",
        "karmagroup.com",
        "karmaexperience",
        "karmajimbaran.com",
        "karmakandara.com",
        "karmakasa"
        "karmalaherizza.com",
        "karmamargaretriver.com",
        "karmamayura.com",
        "karmaminoan.com",
        "karmamykonos.com",
        "karmanormandy.com",
        "karmaodyssey.com",
        "karmapassport.com",
        "karmapelikanos.com",
        "karmaprivilege"
        "karmareef.com",
        "karmaresort",
        "karmaresorts",
        "karmarestaurants.com",
        "karmarottnest.com",
        "karmaroyal",
        "karmasalak.com",
        "karmasalfordhall.com",
        "karmasanctum",
        "karmaspa",
        "karmastmartin",
        "karmaubud.com",
        "karmawinery.com",
        "krgstorage.com",
        "krresidences.com",
        "lepreverger.com",
        "odysseykarma.com",
        "odysseypremier.com",
        "royalbalitimeshare.com",
        "royalperspective.com",
        "royalresorts",
        "sanctumhotel",
        "sanctumsoho",
        "thekarmaclub.com",
        "thekarmacollection",
        "themoleandbadger.com",
        "tiketmurahbali.com",
        "timesharebali.com",
        "wildheartbarandgrill.com",
        "wildheartsoho.com",
        "yuktamasya.com"
    ]

