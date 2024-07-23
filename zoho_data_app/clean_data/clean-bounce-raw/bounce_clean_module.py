import pandas as pd
import numpy as np
from datetime import datetime

import re

def get_desc(message):
    desc = ['smtp; 552 1 Requested mail action aborted, mailbox not found',
            'smtp; 550 5.5.0 Requested action not taken: mailbox unavailable (S2017062302).',
            'smtp;554 5.4.6 Hop count exceeded - possible mail loop',
            'smtp; 550 Requested action not taken: mailbox unavailable',
            'smtp; 550 Mailbox is full / Blocks limit exceeded / Inode limit exceeded',
            'smtp; 550 blocked',
            'smtp;550 5.4.312 Message expired, DNS query failed',
            'mailbox is disabled',
            'Hop count exceeded - possible mail loop',
            'smtp; 550 No Such User Here',
            'Recipient address rejected: Access denied',
            'smtp; 550-The mail server could not deliver mail to',
            'smtp; 550 Unrouteable address',
            'X-Postfix; Host or domain name not found',
            'X-Postfix; Message delivery failed',
            'smtp; 550 No such person at this address.',
            'smtp; 550 5.2.1 This mailbox has been blocked due to inactivity'
            'smtp; 550-The account has been suspended for inactivity 550 A conta do destinatario encontra-se suspensa por inactividade (#5.2.1)',
            'If you believe that this failure is in error, please contact the intended recipient via alternate means']

    # escaped = str.maketrans({"-":  r"\-",
    #                                       "]":  r"\]",
    #                                       "\\": r"\\",
    #                                       "^":  r"\^",
    #                                       "$":  r"\$",
    #                                       "*":  r"\*",
    #                                       ".":  r"\."})

    # desc_correction = desc.translate(escaped)

    if any(substring in message for substring in desc):
    # 👇️ this runs
        delete = 'Yes'
    else:
        delete = 'No'

    return delete
