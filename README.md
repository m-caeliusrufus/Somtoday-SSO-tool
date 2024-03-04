# Somtoday SSO tool
This is a tool to scrape the data from the SomToday API and save them to a XML file when your school is using SSO.
## Installing
Clone this repository -- `git clone https://github.com/m-caeliusrufus/Somtoday-SSO-tool` or just download `somtoday_api.py`
## Setting up
- Get the UUID for your school from `servers.somtoday.nl/organisaties.json`
- Install the following Python libraries:
### Selenium
Run `pip install selenium`
### Requests
Run `pip install requests`
### XmlToDict
Run `pip install xmltodict`
## Using the program
- Run the Python file and enter the uuid for your school
- A browser window will open with the login screen for your school --- this is the real SomToday login screen, I won't be doing anything with your username and password
- After completing login, the browser window will automatically close
- The script will automatically get your data from the API, and you should see your name and SomToday student ID being printed to the screen
- This means that your data has been exported to `leerlingen.xml`
- (optional) You can also get your grades etc. by uncommenting the code for the different GET requests.
