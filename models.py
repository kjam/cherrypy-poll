from db_tools import get_value,set_value,del_value 
from utils import slugify

def create_poll(**kwargs):
    """ This creates the initial poll question. It expects the following key,value pairs:
        question: the poll question
        answer: a list of strings that are the answer choices """
    poll_key = slugify(kwargs.get('question'))
    poll_value = {
        'question': kwargs.get('question'),
    }
    for a in kwargs.get('answer'):
        poll_value[a] = 0
    set_value(poll_key,poll_value)
    return poll_value

def delete_poll(key):
    del_value(key)
    return True

