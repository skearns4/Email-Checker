# Email-Checker
Turns my emailed, plaintext work schedule in to an iCalendar event(s)

I receive a weekly email from an employer containing my schedule for the upcoming week. 
This program will check my email and search for the latest message recieved from the automated schedule mailer.
It will parse the body of the email, strip the desired scheduling information from it, and create a .ics file for each day that I am scheduled to work. 

It is very personalized to handle the format that my schedule is given and the fact that the emails being received are from a Gmail account. It should be fairly easy to customize to handle any schedule as long as it is in a plaintext format. 

Sources: https://yuji.wordpress.com/2011/06/22/python-imaplib-imap-example-with-gmail/, http://pymotw.com/2/imaplib/, http://icalendar.readthedocs.org/en/latest/
