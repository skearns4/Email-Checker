import imaplib
import pytz
import tempfile
import os
import getpass
from icalendar import Calendar, Event, vCalAddress
from datetime import datetime, date

#sign into gmail account
imap_server = imaplib.IMAP4_SSL('imap.gmail.com', 993)
user = raw_input('Username: ')
user = user+'@gmail.com'
password = getpass.getpass()
imap_server.login(user, password)
imap_server.select('Inbox', readonly=True)

#method to create new .ics file for given day, month, and hours
def create_event(year, month, day, hour_start, minute_start, hour_end, minute_end, filename):
    #create calendar and event objects
    cal = Calendar()
    event = Event()
    
    #add schedule info to the event
    event.add('summary', 'Work')
    event.add('dtstart', datetime(year, month, day, hour_start, minute_start, tzinfo=pytz.timezone('US/Eastern')))
    event.add('dtend', datetime(year, month, day, hour_end, minute_end, tzinfo=pytz.timezone('US/Eastern')))
    organizer = vCalAddress('MAILTO:'+user)

    #add event to calendar
    cal.add_component(event)

    #make a temporay directory
    directory = tempfile.mkdtemp()
    #create temp file
    f = open(os.path.join(directory, filename+'.ics'), 'wb')
    #move that file to somewhere easier to access
    os.rename(f.name, "/User/You/Destination/"+filename+".ics")
    #make that file an ical event
    f.write(cal.to_ical())
    #closes the file
    f.close()

#finds email in inbox sent from the automated scheudle mailer
typ, data = imap_server.search(None, 'FROM', "never_reply@website.com")

#gets email data as a list
for num in data[0].split():
    rv, data = imap_server.fetch(num, '(RFC822)')

#closes connection to the gmail server
imap_server.logout()

#converts and nicely formats the information from the email that is required to make a calendar file
sched_as_string = str(data[0])
sched_as_string = sched_as_string[sched_as_string.find("Sunday"):]
sched_as_string = sched_as_string.replace(r'\r', '').replace(r'\n', '').replace(r'\n', '').replace(' ', '').replace(',', '').replace("'", '').replace(')', '')

#create a list of the days of the week
list_of_days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

#uses the days of the week list to make a dictionary object that contains the days of the week as keys and empty strings as values
days_dict = {}
for day_of_week in list_of_days:
    days_dict[day_of_week] = ''

#for each day of the week
#slice the scheduling information from the appropriate part of the string
#make that information the value for that day of the week
for day_of_week in range(0, 7):
    if list_of_days[day_of_week] == 'Saturday':
        days_dict[list_of_days[day_of_week]] = sched_as_string[sched_as_string.find('Saturday'):]
        break
    else:
        days_dict[list_of_days[day_of_week]] = sched_as_string[sched_as_string.find(list_of_days[day_of_week]):sched_as_string.find(list_of_days[day_of_week+1])]

#strip the day of the week from the dictionary values
for day_of_week in days_dict.keys():
    days_dict[day_of_week] = days_dict[day_of_week][(days_dict[day_of_week].find('y')+1):]

#deletes dictionary entires where no hours are not scheduled
for day_of_week in days_dict.keys():
    if len(days_dict[day_of_week]) < 10:
        del(days_dict[day_of_week])
    else:
        days_dict[day_of_week] = days_dict[day_of_week][:20]

#goes through the dictionary to and send scheudle information to create_event for each day
for key, value in days_dict.items():
    mnth = int(value[:2])
    dy = int(value[3:5])
    hr_strt = int(value[5:7])
    min_strt = int(value[8:10])
    hr_end = int(value[13:15])
    min_end = int(value[16:18])
    #make sure the hours are compatible with the 24 hour clock format
    if value[10] is 'P':
        if hr_strt is not 12:
            hr_strt += 12
    if value[18] is 'P':
        if hr_end is not 12:
            hr_end += 12
    #pass day, month, and hours to create_event
    create_event(date.today().year, mnth, dy, hr_strt, min_strt, hr_end, min_end, key)
