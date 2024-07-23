
from setup_api import setup
from mailwizz.endpoint.lists import Lists
import pandas as pd
import json
from pandas import json_normalize


"""
SETUP THE API
"""
setup()

"""
CREATE THE ENDPOINT
"""
endpointLists = Lists()


def load_list():
    response = endpointLists.get_lists(page=1, per_page=10)

    """
    DISPLAY RESPONSE
    """
    json_response = json.loads(response.content)
    df = json_normalize(json_response['data']['records']) 
    
    return response.content


    

def get_one_list():
    
    """
    GET ONE ITEM
    """
    response = endpointLists.get_list('LIST_UID')

    """
    DISPLAY RESPONSE
    """
    print(response.content)

def create_list():
    response = endpointLists.create({
        # required
        'general': {
            'name': 'Test2',  # required
            'description': 'This is a test list, created from the API.',  # required
        },
        'defaults': {
            'from_name': 'Fajar Fatoni',  # required
            'from_email': 'fajar.fatoni@karmagroup.com',  # required
            'reply_to': 'fajar.fatoni@karmagroup.com',  # required
            'subject': 'Hello!',
        },
        'company': {
        'name': 'Karma Concierge',  # required
        'country': 'Indonesia',  # required
        'zone_name': 'Bali',  # required
        'address_1': 'Jl. Raya Kuta No.137, Kuta, Kec. Kuta', # required
        'address_2' : '',
        'city' : 'Badung',
        'zip_code' : '80361',
    }
    })

    print(response.content)
