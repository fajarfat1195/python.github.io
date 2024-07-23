import re

def Norm_Title(s: str):
    return s.title().strip()

def Norm_Cap(s: str):
    return s.capitalize().strip()

def Norm_Low(s: str):
    return s.lower().strip()

def Norm_Email(s):
    s = str(s)
    email = Norm_Low(s)
    email = re.sub(r"\s+", "", email)
    return email.strip()

def checkCountryCode(s: str, y: str):
    if str(s)[:1] == '0':
        s = str(s)[1:]
        
    if y == 'Australia' and str(s)[:2] != '61':
        s = "61"+str(s)
    elif y == 'Austria' and str(s)[:2] != '43':
        s = "43"+str(s)
    elif y == 'Brazil' and str(s)[:2] != '55':
        s = "55"+str(s)
    elif y == 'Canada' and str(s)[:1] != '1':
        s = "1"+str(s)
    elif y == 'France' and str(s)[:2] != '33':
        s = "33"+str(s)
    elif y == 'Germany' and str(s)[:2] != '49':
        s = "49"+str(s)
    elif y == 'Hungary' and str(s)[:2] != '36':
        s = "36"+str(s)
    elif y == 'Indonesia' and str(s)[:2] != '62':
        s = "62"+str(s)
    elif y == 'India' and str(s)[:2] != '91':
        s = "91"+str(s)
    elif y == 'Isle Of Man' and str(s)[:6] != '441624':
        s = "44-1624"+str(s)
    elif y == 'Israel' and str(s)[:3] != '972':
        s = "972"+str(s)
    elif y == 'Italy' and str(s)[:2] != '39':
        s = "39"+str(s)
    elif (y == 'Moldova' or y.__contains__('Moldova')) and str(s)[:3] != '373':
        s = "373"+str(s)
    elif y == 'Netherlands' and str(s)[:2] != '31':
        s = "31"+str(s)
    elif y == 'New Zealand' and str(s)[:2] != '64':
        s = "64"+str(s)
    elif (y == 'Russia' or y.__contains__('Russia')) and str(s)[:1] != '7':
        s = "7"+str(s)
    elif y == 'Singapore' and str(s)[:2] != '65':
        s = "65"+str(s)
    elif y == 'South Africa' and str(s)[:2] != '27':
        s = "27"+str(s)
    elif y == 'Spain' and str(s)[:2] != '34':
        s = "34"+str(s)
    elif y == 'Sweden' and str(s)[:2] != '46':
        s = "46"+str(s)
    elif y == 'Switzerland' and str(s)[:2] != '41':
        s = "41"+str(s)
    elif y == 'Taiwan' and str(s)[:3] != '886':
        s = "886"+str(s)
    elif y == 'United Kingdom' and str(s)[:2] != '44':
        s = "44"+str(s)
    elif y == 'United States' and str(s)[:1] != '1':
        s = "1"+str(s)
    elif y == 'Vietnam' and str(s)[:2] != '84':
        s = "84"+str(s)

    return s

def Norm_Phone(s, y):
    s = str(s)
    s = s.strip().replace('+','').replace('-','').replace(')','').replace('(','').replace('.0','').replace('/','')
    s = re.sub(r"\s+", "", s)
    if s != '' and y != '':
        s = checkCountryCode(s, y)

    return s

def setDateTime():
    from datetime import datetime as dt
    now = dt.today().strftime('%Y-%m-%d %H:%M:%S')
    return str(now)

def setDate():
    from datetime import datetime as dt
    now = dt.today().strftime('%Y-%m-%d')
    return str(now)

def setLang(nat, lang):
    if nat == 'German':
        return 'Deu'
    elif nat == 'British' or nat == 'American' or nat == 'Australian':
        return 'Eng'
    else:
        return lang

def Norm_IDZoho(s):
    s = str(s)
    s = s.strip().replace('zcrm','').replace('_','')
    return s