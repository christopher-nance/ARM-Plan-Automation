# FastPass Plan Automation Script
### Developer: Chris Nance for NASCAR Car Wash
### Version: 1.0

This script will allow automation of Discontinue, Terminate and Switch ARM Plan functions. Each plan takes approx. 5 seconds to modify. 

# Dependencies
## Software
* [Python](https://www.python.org/downloads/)
* [SiteWatch 2014 by DRB](https://drb.com/tunnel_solutions/point-of-sale/sitewatch)
## Modules (Any Version)
* [Colorama](https://pypi.org/project/colorama/)
* [Pandas](https://pypi.org/project/pandas/)
* [Mouse](https://pypi.org/project/mouse/)
* [Keyboard](https://pypi.org/project/keyboard/)
These can all be installed using the pip command: 
~~~
pip install keyboard mouse pandas colorama
~~~
## Data
* CSV File of the customer data exported from SiteManager
  * Include all headers when exporting
  * Use the ARM Customer Analysis Viewer, then Ctrl+P, and export to a text file; then copy the text file contents into the first cell of a CSV file.
* CSV File MUST contain one piece of information in each cell with headers having their own cell. 



# Additional Information
* Python along with the needed modules are usually not accessible from the computer this script needs ot run on, therefore it is suggested that the modules along with the python installer are downloaded to a flashdrive and moved onto the computer that will be running the script. 
* The script MUST be in the same directory as the modules to run properly.
* Due to the way Terminal Controller is used and the proprietary nature of the SiteWatch software bundle, there is no direct way to interact with the controller or database in a safe manner without causing possible corruption in memory. 
* Due to the limitation of Terminal Controller, it is suggested that this script is run on a terminal that will not be used and is running windows 10 or newer in order to speed the process up.
* Due to the limitation of Terminal Controller, this script is a guessing game. Some customers might NOT be modified, it is suggested that a report is run after a run to see if the customers have all been cleared or modified to your content.

# How does it work?
By using the mouse and keyboard libraries we can easily simulate the way an employee would perform various actions on the terminal. A dictionary contains all the X,Y screen coordinates to move the mouse and click on the buttons as well as a keyboard input to agree to prompts or press ok. Additional configuration in SiteManager can be done to enable shortcuts on pages and then modification of this script to completly eliminate the mouse library and simly use shortcuts. 


*No responsibility is taken for any misconfigured or broken passes.*
