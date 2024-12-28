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
    ("Joe Jefferson Masterclass", "2025-01-12 16:05", "2025-01-12 18:00", "room TBA"),
    ("Bill Mann Recital", "2025-01-28 19:20", "2025-01-28 21:00", "MUB101"),
    ("Carli Castillon DMA Recital 3", "2025-02-01 19:20", "2025-02-01 21:00", "MUB101"),
    ("Traditional Music of South America: Angelo Cassanello Bueno Guest Artist Recital", 
     "2025-02-25 17:10", "2025-02-25 18:30", "MUB101"),
    ("Megumi Kanda Chamber Masterclass (BrassFest)", "2025-03-07 12:50", "2025-03-07 14:30", "MUB101"),
    ("Graduate Brass Quintet Recital (BrassFest)", "2025-03-07 17:10", "2025-03-07 18:30", "MUB101"),
    ("Taylor Klonowski Senior Recital", "2025-03-07 19:20", "2025-03-07 21:00", "MUB101"),
    ("Morning Warmups (BrassFest)", "2025-03-08 09:35", "2025-03-08 10:35", "room TBA"),
    ("Patrick Smith Horn Recital (BrassFest)", "2025-03-08 12:50", "2025-03-08 14:30", "MUB101"),
    ("Megumi Kanda Solo Masterclass (BrassFest)", "2025-03-08 13:55", "2025-03-08 15:15", "room TBA"),
    ("Trombone Ensemble Concert (BrassFest)", "2025-03-08 16:05", "2025-03-08 17:30", "UA"),
    ("Megumi Kanda Recital (BrassFest)", "2025-03-09 10:40", "2025-03-09 12:00", "MUB101"),
    ("Finale Concert (BrassFest)", "2025-03-09 11:45", "2025-03-09 13:15", "MUB101"),
    ("Corey Burton DMA Recital 2", "2025-04-04 19:20", "2025-04-04 21:00", "MUB101"),
    ("Ethan Spencer DMA Recital 2", "2025-04-05 19:20", "2025-04-05 21:00", "MUB101"),
    ("Jason Donnelly DMA Recital 1", "2025-04-08 19:20", "2025-04-08 21:00", "MUB101"),
    ("Kang Muscatello Junior Recital", "2025-04-19 13:55", "2025-04-19 15:15", "MUB101"),
]

# Add events to calendar
for event in events:
    summary, start, end, location = event
    start_dt = datetime.strptime(start, "%Y-%m-%d %H:%M")
    end_dt = datetime.strptime(end, "%Y-%m-%d %H:%M")
    cal.add_component(create_event(summary, start_dt, end_dt, location))

# Save to file
with open("required_events_2025.ics", 'wb') as f:
    f.write(cal.to_ical())
