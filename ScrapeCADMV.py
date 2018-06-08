# ===============================================================================
# ScrapeCADMV.py
# 
# Get a list of office visit appointment times for places around the Bay Area from the CA DMV
# See DMV_Info.json under "Bay Area" to edit the list of places
# 
# -------------------------------------------------------------
# *) Install a package manager (ex: pip: https://pip.pypa.io/en/stable/installing/)
# 
# Required Python Packages to Download:
# 	- Mechanize: $pip install mechanize
# 	- BeautifulSoup: $pip install beautifulsoup4
# 
# -------------------------------------------------------------
# Govinda Ram Pingali
# June 6th, 2018 
# ===============================================================================


import mechanize
import cookielib
import ssl
from bs4 import BeautifulSoup

import json
import time
from threading import Event, Thread



class DMVAppointment(object):


	def __init__(self, id, ready=None):
		self.ready = ready
		self.id = id


	def run(self):

# ===============================================================================
# Browser Setup
# ===============================================================================

		# Browser
		br = mechanize.Browser()

		# Cookie Jar
		cj = cookielib.LWPCookieJar()
		br.set_cookiejar(cj)

		# Browser options
		br.set_handle_equiv(True)
		br.set_handle_gzip(True)
		br.set_handle_redirect(True)
		br.set_handle_referer(True)
		br.set_handle_robots(False)

		# Follows refresh 0 but not hangs on refresh > 0
		br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

		# Want debugging messages?
		#br.set_debug_http(True)
		#br.set_debug_redirects(True)
		#br.set_debug_responses(True)

		# User-Agent (this is cheating, okay? okay.)
		br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]


		# Disable SSL Verification
		try:
		    _create_unverified_https_context = ssl._create_unverified_context
		except AttributeError:
		    # Legacy Python that doesn't verify HTTPS certificates by default
		    pass
		else:
		    # Handle target environment that doesn't support HTTPS verification
		    ssl._create_default_https_context = _create_unverified_https_context


# ===============================================================================
# Open Page
# ===============================================================================

		url = 'https://www.dmv.ca.gov/wasapp/foa/clear.do?goTo=officeVisit&localeName=en'
		form_name = "ApptForm" # Method: POST

		# Form To Fill
		FIRSTNAME = 'JANE'
		LASTNAME = 'DOE'
		TELAREA = '123'
		TELPREFIX = '456'
		TELSUFFIX = '7890'
		# OFFICE_ID = "503" # Test SF

		response = br.open(url)
		html = response.read()

		# Select Form
		index = 0
		for form in br.forms():
			if form.name == form_name:
				break
			index += 1

		br.select_form(nr=index)

		# Fill DMV Appointment Form
		br['officeId']=[self.id]
		br['numberItems']=["1"]
		br['taskRID']=["true"]	# RealID. Use 'taskCID' for CA ID or 'taskVR' for Vehicle Registration
		br['firstName']=FIRSTNAME
		br['lastName']=LASTNAME
		br['telArea']=TELAREA
		br['telPrefix']=TELPREFIX
		br['telSuffix']=TELSUFFIX

		# Submit
		br.submit()

		# Make Soup
		soup = BeautifulSoup(br.response().read(), 'html.parser')

		# Extract Content
		office = soup.find("td", {"data-title" : "Office"}).find("p").contents[0].strip()
		appointment = soup.find("td", {"data-title" : "Appointment"}).findAll("p")[1].find("strong").contents[0].strip()

		# Close
		br.close()

		# Result
		print "%s at %s" % (office, appointment)


	def __del__(self):
		self.ready.set()


# Start
print "Next open DMV appointment times in the Bay Area:"


# Read place IDs JSON
with open("CADMV_Info.json") as file:
	data = json.load(file)
	array = data["BayArea"]


# Iterate through all DMV offices and get appointment time for each
for office in array:
	ready = Event()
	program = DMVAppointment(office["officeID"], ready)
	thread = Thread(target=program.run)
	thread.start()
	del program
	ready.wait()
