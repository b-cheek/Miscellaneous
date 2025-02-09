from datetime import datetime
from icalendar import Calendar, Event

# Helper function to create an event
def create_event(summary, start_dt, end_dt, location):
    event = Event()
    event.add('summary', summary)
    event.add('dtstart', start_dt)
    event.add('dtend', end_dt)
    event.add('location', location)
    return event

# Initialize calendar
cal = Calendar()

# Define events (start times, durations, and locations)
events = [
    ("Swazz at Baby J's", "2025-02-21 20:00", "2025-02-21 22:00", "Baby J's"),
    ("Brass Band Concert", "2025-02-25 19:20", "2025-02-25 20:10", "University Auditorium"),
    ("Swazz at Gator Bait", "2025-03-28 18:00", "2025-03-28 21:00", "Gator Bait"),
    ("UF Jazz Concert", "2025-04-03 19:20", "2025-04-03 21:00", "University Auditorium"),
    ("Swazz at Gator Bait", "2025-04-04 18:00", "2025-04-04 21:00", "Gator Bait"),
    ("TBA Jazz Combo", "2025-04-06 12:00", "2025-04-06 15:00", "Lake Wauburg North Shore?"),
    ("Swazz at Gator Bait", "2025-04-25 18:00", "2025-04-25 21:00", "Gator Bait"),
]

# Add events to calendar
for event in events:
    summary, start, end, location = event
    start_dt = datetime.strptime(start, "%Y-%m-%d %H:%M")
    end_dt = datetime.strptime(end, "%Y-%m-%d %H:%M")
    cal.add_component(create_event(summary, start_dt, end_dt, location))

# Save to file
with open("gigs_4_taylor.ics", 'wb') as f:
    f.write(cal.to_ical())
