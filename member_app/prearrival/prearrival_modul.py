import pandas as pd

import re

def location_correction(location):
    if (location == 'Karma Sobek, Sharm El-Sheikh'):
        location_correction = 'Karma Sobek'

    elif (location == 'Karma Sitabani, Corbett'):
        location_correction = 'Karma Sitabani'

    elif (location == 'Karma Haveli, Jaipur'):
        location_correction = 'Karma Haveli'

    elif (location == 'Karma Golden Camp, Jaisalmer'):
        location_correction = 'Karma Golden Camp'

    elif (location == 'Karma Chakra, Kerala'):
        location_correction = 'Karma Chakra'

    elif (location == 'Karma Munnar, Kerala'):
        location_correction = 'Karma Munnar'

    elif (location == 'Karma Seven Lakes, Udaipur'):
        location_correction = 'Karma Seven Lakes'

    elif (location == 'Karma Utopia, Manali'):
        location_correction = 'Karma Utopia'

    elif (location == 'Karma Seven Lakes, Udaipur'):
        location_correction = 'Karma Seven Lakes'

    elif (location == 'Karma St. Martins'):
        location_correction = 'Karma St. Martin\'s'

    elif (location == 'Karma Cay Tre'):
        location_correction = 'Karma Cây Tre'

    elif (location == 'Karma Royal Monterio'):
        location_correction = 'Karma Royal MonteRio'

    elif (location == 'Karma Borgo Di Colleoli'):
        location_correction = 'Karma Borgo di Colleoli'
    
    elif (location == 'Chateau de Samary, Carcassonne'):
        location_correction = 'Karma Chateau de Samary'

    else:
        location_correction = location
    return location_correction


def get_resort():
    resort_list = ['Karma Karnak', 
                   'Karma Sobek, Sharm El-Sheikh',
                   'Chateau de Samary, Carcassonne',
                   'Karma Bavaria',
                   'Karma Minoan',
                   'Karma Sunshine Village',
                   'Karma Lakewood, Mahabaleshwar',
                   'Karma Sitabani, Corbett',
                   'Karma Royal Haathi Mahal',
                   'Karma Royal Palms',
                   'Karma Royal Monterio',
                   'Karma Haveli, Jaipur',
                   'Karma Martam Retreat',
                   'Karma Golden Camp, Jaisalmer',
                   'Karma Chakra, Kerala',
                   'Karma Munnar, Kerala',
                   'Karma Seven Lakes, Udaipur',
                   'Karma Utopia, Manali',
                   'Karma Kandara',
                   'KRR @ Karma Kandara',
                   'Karma Kandara Final Release',
                   'Karma Royal Candidasa',
                   'Karma Royal Sanur',
                   'Karma Jimbaran',
                   'Karma Royal Jimbaran',
                   'Karma Borgo Di Colleoli',
                   'Karma La Herriza',
                   'Karma Royal Boat Lagoon',
                   'Karma St. Martins',
                   'Karma Lake of Menteith',
                   'Karma Salford Hall',
                   'Karma Song Hoai',
                   'Karma Cay Tre',
                   'Karma Nomad'
                   ]
    return resort_list