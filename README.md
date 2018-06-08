## CA DMV Appointments
It is quite a pain to look for an appointment time on the DMV website, especially if want one soon(ish), and don't want to wait in line from 5:00am.

This python script queries the DMV site for the next available appointment from various locations (office IDs) around California. A subset of San Francisco Bay Area offices is currently used.

**To run:** python ScrapeCADMV.py

#### Upcoming
A chron job that will run every so often, find an acceptable time and place, send an SMS alert to you asking for confirmation, if "YES", then make the booking. Your very own DMV Appointment Booking Assistant that will not get bored of dialling and doesn't need a lunch break.

#### Required Packages
- Mechanize (http://mechanize.readthedocs.io/en/latest/#)
- Beautiful Soup (http://mechanize.readthedocs.io/en/latest/#)