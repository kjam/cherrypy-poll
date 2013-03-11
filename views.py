from db_tools import get_value,set_value,del_value 
from utils import slugify

def cast_vote(poll_key,choice):
    poll = get_value(poll_key)
    for c in poll['choices']:
        if c['id'] == int(choice):
            c['value'] += 1
    set_value(poll_key,poll)
    return poll

def get_global_links():
    return [{
        'name': 'Add a poll',
        'url': '/polls/add',
        },
        {
        'name': 'Home',
        'url': '/'
        },
        {
        'name': 'Poll list',
        'url': '/polls',
        }]

def get_poll(key):
    poll = get_value(key)
    return poll


def get_polls():
    poll_list = []
    published_polls = get_value('published_polls')
    if not published_polls:
        set_value('published_polls',[])
    for p in published_polls:
        poll = get_value(p)
        poll_list.append(poll)
    return poll_list

def publish_poll(key):
    published_polls = get_value('published_polls')
    if not published_polls:               
        set_value('published_polls',[])   
    if key not in published_polls:
        published_polls.append(key)
        set_value('published_polls',published_polls)

def unpublish_polls(key):
    published_polls = get_value('published_polls')   
    if not published_polls:               
        set_value('published_polls',[])  
    if key in published_polls:
        published_polls.remove(key)
        set_value('published_polls',published_polls)

def add_poll(**kwargs):
    choices_arr = []
    count = 1
    poll_dict = {}
    poll_dict['question'] = kwargs.get('question')
    for k,v in kwargs.items():
        if 'choice' not in k: continue
        choice_dict = {
            'id': count,
            'text': v,
            'value': 0
        }
        choices_arr.append(choice_dict)
        count += 1
    slug = slugify(kwargs.get('question')) 
    poll_dict['slug'] = slug
    poll_dict['choices'] = choices_arr
    set_value(slug,poll_dict)
    if kwargs.get('publish'):
        publish_poll(slug)

def edit_poll(**kwargs):
    choices_arr = []
    poll = get_poll(str(kwargs.get('slug')))
    poll_dict = {}
    poll_dict['question'] = kwargs.get('question')
    for k,v in kwargs.items():
        if 'choice' not in k: continue
        this_choice = [c for c in poll.get('choices') if int(k.strip('choice')) == c.get('id')]
        if not len(this_choice):
            return False
        else:
            this_choice = this_choice[0]
        choice_dict = {
            'id': this_choice.get('id'),
            'text': v,
            'value': this_choice.get('value'),
        }
        choices_arr.append(choice_dict)
    slug = str(kwargs.get('slug'))
    poll_dict['slug'] = slug
    poll_dict['choices'] = choices_arr
    set_value(slug,poll_dict)
    if kwargs.get('publish'):
        publish_poll(slug)
    else:
        unpublish_poll(slug)
    return poll_dict
