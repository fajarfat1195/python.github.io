import pandas as pd
import re

def find_deleted_email(df, df_columns):
    
    filter_deleted_email = '@Karmagroup.com|@karmasalfordhall.com|@karmaclub.com|Concierge.india@krresidences.com|test@'
    count_deleted_email = df.loc[df[df_columns].str.contains(filter_deleted_email, flags=re.I, regex=True)].shape[0]

    # replace email value yang memiliki tanda OTA
    df.loc[df[df_columns].str.contains(filter_deleted_email, flags=re.I, regex=True), df_columns] = 'Delete Email'
    return count_deleted_email

def delete_email(df, df_columns):
    
    df.drop(df.loc[df[df_columns] == 'Delete Email'].index, inplace=True)
    df.reset_index(drop=True, inplace=True)

    count_after_delete_email = df.shape[0]

    return count_after_delete_email

def email_correction(df, df_columns):
    
    list_correction_mail = ['@mal\.','@mai\.']
    df[df_columns].replace('|'.join(list_correction_mail), '@mail.', regex=True, inplace=True)
    
    list_correction_gmail = [
        '@gmil\.','@gmaail\.','@gmailo\.','@gmai\.','@gmails\.','@gmal\.','@gmwil\.','@gamail\.','@gmailk\.','@gmzil\.', '@gtmail\.',
        '@gjail\.','@gmaip\.','@gmasil\.','@gmcil\.','@gail\.','@gimail\.','@gmailo\.','@gmaiol\.','@gmaili\.','@fgmail\.','@gamil\.'
        ]
    df[df_columns].replace('|'.join(list_correction_gmail), '@gmail.', regex=True, inplace=True)

    list_correction_gmail_com = ['@gmail\.cm','@gmailc\.om', '@gmail\.clm', '@gmail\.con','@@gmail\.clm','@gmail\.coj','@gmail\.cok','@gmail\.c0m',
                                 '@gmail\.comQ', '@gmail\.co$', '@gmail\.vom', '@gmail\.cim']
    df[df_columns].replace('|'.join(list_correction_gmail_com), '@gmail.com', regex=True, inplace=True)

    list_correction_hotmail = ['@jotmail\.','@hotmil\.','@hotlamil\.','@h0tmail\.','@hotjail\.','@hotmaio\.']
    df[df_columns].replace('|'.join(list_correction_hotmail), '@hotmail.', regex=True, inplace=True)

    list_correction_hotmail_com = ['@jotmail\.dom']
    df[df_columns].replace('|'.join(list_correction_hotmail_com), '@hotmail.com', regex=True, inplace=True)
    

    list_correction_yahoo = ['@yahho\.','@yaho\.','@gyahoo\.','@yahoom\.', '@yaoo\.','@yehoo\.','@yahio\.','@rotmail\.','@yshoo\.']
    df[df_columns].replace('|'.join(list_correction_yahoo), '@yahoo.', regex=True, inplace=True)

    list_correction_ymail = ['@y7mail\.']
    df[df_columns].replace('|'.join(list_correction_ymail), '@ymail.', regex=True, inplace=True)

def get_list_UK_EU():

    list_UK_EU = ['Albania','Andorra','Armenia','Austria','Azerbaijan','Belarus','Belgium','Bosnia','Herzegovina','Bulgaria','Croatia','Cyprus','Czech Republic','Denmark','Estonia','Finland',
    'France','French Guiana','Georgia','Germany','Greece','Guadeloupe','Hungary','Iceland','Ireland','Italy','Kazakhstan','Kosovo','Latvia','Liechtenstein','Lithuania','Luxembourg','Malta',
    'Martinique','Mayotte','Moldova','Monaco','Montenegro','Netherlands','North Macedonia','Norway','Poland','Portugal','Réunion','Romania','Russia','Saint Martin','San Marino','Serbia','Slovakia',
    'Slovenia','Spain','Sweden','Switzerland','Turkey','Ukraine','United Kingdom','Vatican','England', 'Scotland', 'Wales', 'Channel Islands']

    return list_UK_EU

def get_list_Others():
    
    list_Others = ['Australia','Afghanistan','Åland Islands','Algeria','American Samoa','Angola','Anguilla','Antigua and Barbuda','Argentina','Aruba','Ascension','Australia',
    'Australian Antarctic Territory','Australian External Territories','Bahamas','Bahrain','Bangladesh','Barbados','Barbuda','Belize','Benin','Bermuda','Bhutan','Bolivia','Bonaire','Botswana',
    'Brazil','British Indian Ocean Territory','British Virgin Islands','Brunei Darussalam', 'Brunei','Burkina Faso','Burundi','Cabo Verde','Cambodia','Cameroon','Canada','Caribbean Netherlands',
    'Cayman Islands','Central African Republic','Chad','Chatham Island','Chile','China','Christmas Island','Cocos (Keeling) Islands','Colombia','Comoros','Congo',
    'Congo, Democratic Republic of the (Zaire) ','Cook Islands','Costa Rica','Cuba','Curaçao','Diego Garcia','Djibouti','Dominica','Dominican Republic','East Timor','Easter Island','Ecuador',
    'Egypt','El Salvador','Equatorial Guinea','Eritrea','Ethiopia','Falkland Islands','Faroe Islands','Fiji','French Antilles','French Polynesia','Gabon','Gambia','Ghana','Gibraltar','Greenland',
    'Grenada','Guam','Guatemala','Guernsey','Guinea','Guinea-Bissau','Guyana','Haiti','Honduras','Hong Kong','Indonesia','Iran','Iraq','Isle of Man','Israel','IvoryCoast','Jamaica','Jan Mayen','Japan',
    'Jersey','Jordan','Kenya','Kiribati','Korea, North','Korea, South','Kuwait','Kyrgyzstan','Laos','Lebanon','Lesotho','Liberia','Libya','Macau','Madagascar','Malawi','Malaysia','Maldives','Mali',
    'Marshall Islands','Mauritania','Mauritius','Mexico','Micronesia','MidwayIsland','Mongolia','Montserrat','Morocco','Mozambique','Myanmar','Nagorno-Karabakh','Namibia','Nauru','Nepal','Nevis',
    'New Caledonia','New Zealand','Nicaragua','Niger','Nigeria','Niue','Norfolk Island','Northern Cyprus','Northern Mariana Islands','Oman','Pakistan','Palau','Palestine, State of','Panama',
    'Papua New Guinea','Paraguay','Peru','Philippines','Pitcairn Islands','Puerto Rico','Qatar','Rwanda','Saba','Saint Barthélemy','Saint Helena','Saint Kitts and Nevis','Saint Lucia',
    'Saint Pierre and Miquelon','Saint Vincent and the Grenadines','Samoa','São Tomé and Príncipe','Saudi Arabia','Senegal','Seychelles','Sierra Leone','Singapore','Sint Eustatius','Sint Maarten',
    'Solomon Islands','Somalia','South Africa','South Georgia and the South Sandwich Islands','South Ossetia','South Sudan','Sri Lanka','Sudan','Suriname','Svalbard','Swaziland','Syria','Taiwan',
    'Tajikistan','Tanzania','Thailand','Togo','Tokelau','Tonga','Transnistria','Trinidad and Tobago','Tristan da Cunha','Tunisia','Turkmenistan','Turks and Caicos Islands','Tuvalu','Uganda',
    'United Arab Emirates','United States','Uruguay','US Virgin Islands','Uzbekistan','Vanuatu','Venezuela','Vietnam','Wake Island','Wallis and Futuna','Yemen','Zambia','Zanzibar','Zimbabwe', 
    'USA', 'Burma', 'Korea, Rep of (North)', 'Korea, Rep of (South)', 'Palestine']

    return list_Others

