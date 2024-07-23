from setup_api import setup
from mailwizz.endpoint.lists import Lists

"""
SETUP THE API
"""
setup()

"""
CREATE THE ENDPOINT
"""
endpointLists = Lists()


"""
"""
response = endpointLists.get_lists(page=1, per_page=10)

"""
DISPLAY RESPONSE
"""
print(response.content)


"""
GET ONE ITEM
"""
response = endpointLists.get_list('LIST_UID')

"""
DISPLAY RESPONSE
"""
print(response.content)
