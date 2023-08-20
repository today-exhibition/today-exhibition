import datetime


def encode_exhibition_title(title):
    title = title.replace('"', "&quot;")
    title = title.replace("'", "&apos;")
    return title

def encode_date(date, form):
    return datetime.datetime.strptime(date, form).date()

def encode_gallery_name(name):
    name = name.replace("(", " ")
    name = name.replace(")", " ")
    return name

def encode_artist_name(artist_string):
    artist_list = artist_string.split(',')
    return artist_list

def is_free(price):
    if price in ['무료', '무료관람', '무료 관람', '관람비 무료']:
        return True
    return False

def is_artist(artist_name):
    if not artist_name:
        return False
    elif '명' in artist_name:
        return False
    else:
        return True