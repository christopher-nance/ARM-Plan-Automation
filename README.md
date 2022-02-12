# FastPass Plan Automation Script
### Chris Nance for NASCAR Car Wash
### Version 1.0

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
## Data
* CSV File of the customer data exported from SiteManager
  * Include all headers when exporting
  * Use the ARM Customer Analysis Viewer, then Ctrl+P, and export to a text file; then copy the text file contents into the first cell of a CSV file.
* CSV File MUST contain one piece of information in each cell with headers having their own cell. 

These can all be installed using the pip command: 
~~~
pip install keyboard mouse pandas colorama
~~~

# Additional Information
* Python along with the needed modules are usually not accessible from the computer this script needs ot run on, therefore it is suggested that the modules along with the python installer are downloaded to a flashdrive and moved onto the computer that will be running the script. 
* The script MUST be in the same directory as the modules to run properly.


*No responsibility is taken for any misconfigured or broken passes.*
