import uuid
import random
import string

def generate_id():
    return str(uuid.uuid4())

def generate_ticket():
    return 'TKT-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
