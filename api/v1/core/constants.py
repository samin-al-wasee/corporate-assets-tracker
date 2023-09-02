MODEL_CHARFIELD_MIN_LENGTH = 8
MODEL_CHARFIELD_MAX_LENGTH = 128
ID_LENGTH = 8
SERIAL_LENGTH = 16


DEPARTMENTS = [
    ("ITC", "Information Technology"),
    ("HRC", "Human Resource"),
    ("DEV", "Software Development"),
    ("SQA", "Software Quality Assurance"),
    ("MKT", "Sales and Marketing"),
    ("FIN", "Finance"),
]

DEVICE_TYPES = [
    ("MOB", "Samartphone"),
    ("LAP", "Laptop"),
    ("TAB", "Tablet"),
]

DEVICE_AVAILABILITY = [
    ("AVAILABLE", "Avaialble"),
    ("IN_USE", "Occupied"),
    ("MAINTENANCE", "Under maintenance or being repaired"),
    ("LOST", "Lost, stolen or permamnently damaged"),
]

DEVICE_LOG_TYPES = [
    ("ASSIGNED", "Assigned to an employee"),
    ("RETURNED", "Returned by the assigned employee"),
    ("SENT_FOR_MAINTENANCE", "Sent for maintenance"),
    ("RETURNED_FROM_MAINTENANCE", "Returned from maintenance"),
    ("LOST", "Went missing"),
    ("FOUND", "Found"),
]
