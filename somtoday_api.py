## Import different libraries
import json
import time
from urllib.parse import urlparse, parse_qs
from selenium import webdriver
import requests
import xmltodict

## Store some constants
client_id = 'somtoday-leerling-native'
SCHOOL_UUID = input("School UUID ")

## Token flow
def get_organisation(uuid):
    response = requests.get('https://raw.githubusercontent.com/NONtoday/organisaties.json/refs/heads/main/organisaties-formatted.json')
    data = response.json()
    school = next((instelling for instelling in data[0]['instellingen'] if instelling['uuid'] == uuid), None)
    if school:
        return school
    else:
        raise ValueError('No school found')

school = get_organisation(SCHOOL_UUID)
base_url = "https://somtoday.nl/oauth2/authorize?redirect_uri=somtoday://nl.topicus.somtoday.leerling/oauth/callback&client_id={CLIENT_ID}&response_type=code&prompt=login&scope=openid&code_challenge=tCqjy6FPb1kdOfvSa43D8a7j8FLDmKFCAz8EdRGdtQA&code_challenge_method=S256&tenant_uuid={TENANT_UUID}".format(CLIENT_ID=client_id, TENANT_UUID=school['uuid'])
print(f"Logging into {school['naam']} with ID: {school['uuid']}")

browser = webdriver.Chrome()
browser.get(base_url)

start_time = time.time()
while True:
    elapsed_time = time.time() - start_time
    if elapsed_time >= 60:  # Can be modified
        print("Timeout: 1 minute elapsed")
        break
    
    console_logs = browser.get_log('browser')
    for log_entry in console_logs:
        if 'Failed to launch' in log_entry['message']:
            url = log_entry['message'].split("'")[1]
            code = parse_qs(urlparse(url).query)['code'][0]

            payload = {
                'grant_type': 'authorization_code',
                'redirect_uri': 'somtoday://nl.topicus.somtoday.leerling/oauth/callback',
                'code_verifier': 't9b9-QCBB3hwdYa3UW2U2c9hhrhNzDdPww8Xp6wETWQ',
                'code': code,
                'scope': 'openid',
                'client_id': client_id
            }

            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            response = requests.post('https://somtoday.nl/oauth2/token', data=payload, headers=headers)
            token_data = response.json()
            # optional -- with open('token.json', 'w') as token_file:
            # optional -- json.dump(token_data, token_file)
            print('Saved token.')
            browser.quit()
            break
    else:
        time.sleep(1)
        continue
    break

# Refresh token
refresh = token_data['refresh_token']
payload = {'grant_type': 'refresh_token',
           'refresh_token': refresh,
           'client_id': client_id}
refresh_req = requests.post('https://somtoday.nl/oauth2/token',data=payload)
access_json = refresh_req.text

# Set access token
access_dict = json.loads(access_json)
code = access_dict['access_token']
code = "Bearer "+code
headers = {'authorization': code}

## Get student info
leerlingen = requests.get('https://api.somtoday.nl/rest/v1/leerlingen',headers=headers)
if leerlingen.status_code != 206:   # debugging
    print(leerlingen.status_code, leerlingen.headers)
else:
    f = open("leerlingen.xml", "w")
    f.write(leerlingen.text)
    f.close()
    xml_data = leerlingen.text
    data_dict = xmltodict.parse(xml_data)
    naam = data_dict['co:items']['rLeerling']['roepnaam'] + " " + data_dict['co:items']['rLeerling']['achternaam']
    leerling_id = data_dict['co:items']['rLeerling']['co:link']['@id']
    print("Name: "+naam+" ; ID: "+leerling_id)

    # Get more information (uncomment if needed)
    # Get grades
    """ cijfers = requests.get('https://api.somtoday.nl/rest/v1/resultaten/huidigVoorLeerling/'+leerling_id,headers=headers)
    f = open("cijfers.xml", "w")
    f.write(cijfers.text)
    f.close() """
    
    # Get schedule
    """ afspraken = requests.get('https://api.somtoday.nl/rest/v1/afspraken',headers=headers)
    f = open("afspraken.xml", "w")
    f.write(afspraken.text)
    f.close() """

    # Get absence
    """ absentie = requests.get('https://api.somtoday.nl/rest/v1/absentiemeldingen',headers=headers)
    f = open("absentie.xml", "w")
    f.write(absentie.text)
    f.close() """

    # Get study guides
    """ studiewijzers = requests.get('https://api.somtoday.nl/rest/v1/studiewijzers',headers=headers)
    f = open("studiewijzer.xml", "w")
    f.write(studiewijzers.text)
    f.close() """

    # Get subjects
    """ vakken = requests.get('https://api.somtoday.nl/rest/v1/vakken',headers=headers)
    f = open("vakken.xml", "w")
    f.write(vakken.text)
    f.close() """

    # Get account info
    """ account = requests.get('https://api.somtoday.nl/rest/v1/account',headers=headers)
    f = open("account.xml", "w")
    f.write(account.text)
    f.close() """

    # Get school years
    """ schooljaren = requests.get('https://api.somtoday.nl/rest/v1/schooljaren',headers=headers)
    f = open("schooljaren.xml", "w")
    f.write(schooljaren.text)
    f.close() """

    # Get enrolled subjects
    """ vakkeuzes = requests.get('https://api.somtoday.nl/rest/v1/vakkeuzes',headers=headers)
    f = open("vakkeuzes.xml", "w")
    f.write(vakkeuzes.text)
    f.close() """

    # Get 'waarnemingen'
    """ waarnemingen = requests.get('https://api.somtoday.nl/rest/v1/waarnemingen',headers=headers)
    f = open("waarnemingen.xml", "w")
    f.write(waarnemingen.text)
    f.close() """
