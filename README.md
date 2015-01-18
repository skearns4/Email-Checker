# Email-Checker
Turns my emailed, plaintext work schedule in to an iCalendar event(s)

I recieve a weekly email from an employer containing my schedule for the upcoming week. 
This program will check my email and search for the latest message recieved from the automated schedule mailer.
It will parse the body of the email, strip the desired scheduling information from it, and create a .ics file for each day that I am scheduled to work. 

It is very personalized to handle the format that my schedule is given. It should be fairly easy to customize to handle any schedule as long as it is in a plaintext format. 

Ideally, I would like to have the program add the event to my calendar by itself or at least send the .ics file via email. But, for now, creating the events and placing them on my desktop works well enough for my needs. 
