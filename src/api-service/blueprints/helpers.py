# Helper Functions
import re

def meta(status_code, message):
    return { 'http_code': status_code, 'message': message }

def isvalidEmail(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) 
