## CA DMV Appointments
It is quite a pain to look for an appointment time on the DMV website, especially if you want one soon(ish), and don't want to wait in line from 5:00am.

This python script queries the DMV site for the next available appointment from various locations (office IDs) around California. A subset of San Francisco Bay Area offices is currently used.
Then, given a search critera (in this case, the month of June), the script will go ahead and make you an appointment at the DMV :)

**To run:** python ScrapeCADMV.py

#### Upcoming
A chron job that will run every so often.
Get the email confirmation from the DMV working.

#### Required Packages
- Mechanize (http://mechanize.readthedocs.io/en/latest/#)
- Beautiful Soup (http://mechanize.readthedocs.io/en/latest/#)