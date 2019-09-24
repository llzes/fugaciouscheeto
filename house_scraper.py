from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from time import gmtime, strftime

# Get the data from the source
url = "https://www.house.gov/representatives"
url_req = urlopen(Request(url, headers={'User-Agent': 'Mozilla'}))
raw_html = BeautifulSoup(url_req, "lxml")
html = raw_html.prettify() 

# Archive data
dir_path = "archive/house/"
time_stamp = strftime("%Y-%m-%dT%H:%M:%S", gmtime())

# # Archive HTML with a timestamp
file_name = dir_path + "html/house-" + time_stamp + ".html"
file = open(file_name, "w")
file.write(str(html))
file.close()

# Archive JSON with a timestamp
json_file_name = dir_path + "json/house-" + time_stamp + ".json"
json = open(json_file_name, "w")
json.write("{\n\t\"members\": [\n")

all_representatives = []

representatives = raw_html("tr")
for representative in representatives[498:]:
    information = representative("td")
    if len(information) > 0:
        full_name = information[0]
        state_district = information[1]
        party = information[2]
        office_room = information[3]
        phone = information[4]
        website = information[0].find("a").get("href")
        committee_assignments = information[5]

    # Pretty printing
    tab = "\t\t\t"

    # Escape quotes in names
    get_name = str(full_name.get_text())
    formatted_name = get_name.replace('"', r'\"')

    # Get first and last name separately
    last_name, first_name = formatted_name.split(",")

    # Get state and district separately
    get_state_district = str(state_district.get_text()).strip()
    state, district = get_state_district.rsplit(" ", 1)
    if district == "Large":
        state, district, district_large = get_state_district.rsplit(" ", 2)
        district = district + " " + district_large

    # JSON 
    print_name = tab + "\"full_name\": \"" + first_name.strip() + " " + last_name.strip() + "\",\n"
    print_first_name = tab + "\"first_name\": \"" + first_name.strip() + "\",\n"
    print_last_name = tab + "\"last_name\": \"" + last_name.strip() + "\",\n"
    print_state_district = tab + "\"state_district\": \"" + get_state_district + "\",\n"
    print_state = tab + "\"state\": \"" + state + "\",\n"
    print_district = tab + "\"district\": \"" + district + "\",\n"
    print_party = tab + "\"party\": \"" + str(party.get_text()).strip() + "\",\n"
    print_office_room = tab + "\"office_room\": \"" + str(office_room.get_text()).strip()  + "\",\n"
    print_phone = tab + "\"phone\": \"" + str(phone.get_text()).strip() + "\",\n"
    print_website = tab + "\"website\": \"" + website + "\",\n"
    print_committee_assignments = ( tab + "\"committee_assignments\": [\"" +
                                    str(committee_assignments.get_text('", "', strip=True)).strip() + "\"]\n" )
    print_all = (
                    "\t\t{\n" +
                    print_name +
                    print_first_name +
                    print_last_name +
                    print_state_district +
                    print_state +
                    print_district +
                    print_party +
                    print_office_room +
                    print_phone +
                    print_website +
                    print_committee_assignments +
                    "\t\t},\n"
                )

    # Remove trailing comma at end of JSON
    if representative == representatives[-1]:
        print_all = print_all[:-2] + "\n\t]\n}"

    json.write(print_all)

json.close()
