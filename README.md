# FastPass Modification Automater
### Developer: Chris Nance for NASCAR Car Wash
### Version: 2.0

## Description
This script will automatically iterate through a pandas dataframe and mdify customer FastPass plans to your needs. This includes Discontinuations, Terminations, Switching Plans, Mass-Sell into a club plan. The Terminal Controller API (TerminalControllerAPI.py) allows for python scripts to simply call functions that will perform actions in Terminal Controller. 

## Instructions
Run the ARM Plan Modification Script using python. Please ensure the TerminalControllerAPI.py script is on your PATH or in the same directory as the ARM Plan Modification Script.

Ensure that you have the proper keybindings setup in SiteManager first! Either create your own or set up a page to have the default mapping below: 

    'FastPass_1':        ['Alt', 'a'], #  FastPass
    'FastPass_2':     ['Alt', 'b'], #  FastPass
    'FastPass_3':         ['Alt', 'c'], #  FastPass
    'FastPass_4':      ['Alt', 'd'], #  FastPass

    'FindAccount_Name':     ['Alt', 'e'], # Find Account with Search Name (Last,First)
    'FindAccount_FPcode':   ['Alt', 'f'], # Find Account with FastPass Number
    'FindAccount_PCcode':   ['Alt', 'g'], # Find Account with PC Code
    'FindAccount_CC':       ['Alt', 'h'], # Find Account with Credit Card Number
    'FastPass_Phone':       ['Alt', 'i'], # Find Account with Phone Number

    'Tender_ARM_CC':        ['Alt', 'j'], # Tender Current Sale w/ ARM CC on File
    'Tender_Cash':          ['Alt', 'k'], # Tender Current Sale w/ CASH

    'Discontinue':          ['Alt', 'l'], # Add 'Discontinue' item to the current sale
    'Terminate':            ['Alt', 'm'], # Add 'Terminate' item to the current sale
    'Switch':               ['Alt', 'n'], # Add 'Switch' item to the current sale

    'OneTimeMsg_Enable':    ['Alt', 'o'], # Enable the one-time message to show up for the customer. 
    'OneTimeMsg_Disable':   ['Alt', 'p'], # Disable the one-time message to show up for the customer. (This should not be used, the customer will disable it via transitions in SiteManager)

    'OpenNewSale':          ['Alt', 'q'], # Opens a new sale
    'ReleaseSale':          ['Alt', 'r'], # Releases the current sale

# Dependencies
## Software
* [Python 3.10](https://www.python.org/downloads/)
* [SiteWatch 2014 (Version 22.10.4) by DRB](https://drb.com/tunnel_solutions/point-of-sale/sitewatch)
## Modules (Any Version)
* [Colorama](https://pypi.org/project/colorama/)
* [Pandas](https://pypi.org/project/pandas/)
* [Mouse](https://pypi.org/project/mouse/)
* [Keyboard](https://pypi.org/project/keyboard/)
* [Clipboard](https://pypi.org/project/clipboard/)
These can all be installed using the pip command: 
~~~
pip install keyboard mouse pandas colorama clipboard
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
* Due to the limitation of Terminal Controller, this script is a guessing game. Some customers might NOT be modified, it is suggested that a report is run after a run to see if the customers have all been cleared or modified to your content. Most customers will be modified. Do not attempt to speed up the timeouts within the API. They have been optimized. Incresing them would be fine if needed.

# How does it work?
By using the mouse and keyboard libraries we can easily simulate the way an employee would perform various actions on the terminal. A dictionary contains all the keybindings setup in SiteManager's Terminal Pages page. The API will then be able to input these keybindings in sequence of events needed faster than an employee.


*No responsibility is taken for any misconfigured or broken passes.*
