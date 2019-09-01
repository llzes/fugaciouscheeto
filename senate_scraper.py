from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from time import gmtime, strftime

# Get the data from the source
url = "https://www.senate.gov/general/contact_information/senators_cfm.xml"
url_req = urlopen(Request(url, headers={'User-Agent': 'Mozilla'}))
xml = BeautifulSoup(url_req, "xml")

# Archive data
dir_path = "archive/senate/"
time_stamp = strftime("%Y-%m-%dT%H:%M:%S", gmtime())

# Archive XML with a timestamp
file_name = dir_path + "xml/senators-" + time_stamp + ".xml"
file = open(file_name, "w")
file.write(str(xml))
file.close()

# Archive JSON with a timestamp
json_file_name = dir_path + "json/senators-" + time_stamp + ".json"
json = open(json_file_name, "w")
json.write("{\n\t\"members\": [\n")

senators = xml.find_all("member")
for senator in senators:
    # All possible XML elements for senators
    full_name = senator.find("member_full")
    last_name = senator.find("last_name")
    first_name = senator.find("first_name")
    party = senator.find("party")
    state = senator.find("state")
    address = senator.find("address")
    phone = senator.find("phone")
    email = senator.find("email")
    website = senator.find("website")
    senate_class = senator.find("class")
    bioguide_id = senator.find("bioguide")

    # Pretty printing
    tab = "\t\t\t"

    # Remove newline from specific addresses
    get_address = str(address.get_text())
    formatted_address = ""
    if "\n" in str(address.get_text()):
        formatted_address.join(str(address.get_text).strip("\n"))
        get_address = formatted_address

    # JSON 
    print_name = tab + "\"fullname\": \"" + str(first_name.get_text()) + " " + str(last_name.get_text()) + "\",\n"
    print_state = tab + "\"state\": \"" + str(state.get_text()) + "\",\n"
    print_party = tab + "\"party\": \"" + str(party.get_text()) + "\",\n"
    print_address = tab + "\"address\": \"" + get_address  + "\",\n"
    print_phone = tab + "\"phone\": \"" + str(phone.get_text()) + "\",\n"
    print_email = tab + "\"email\": \"" + str(email.get_text()) + "\",\n"
    print_website = tab + "\"website\": \"" + str(website.get_text()) + "\",\n"
    print_senate_class = tab + "\"senate_class\": \"" + str(senate_class.get_text()) + "\"\n"
    print_all = (
                    "\t\t{\n" +
                    print_name +
                    print_state +
                    print_party +
                    print_address +
                    print_phone +
                    print_email +
                    print_website +
                    print_senate_class +
                    "\t\t},\n"
                )

    # Remove trailing comma at end of JSON
    if senator == senators[-1]:
        print_all = print_all[:-2] + "\n\t]\n}"

    json.write(print_all)

json.close()
