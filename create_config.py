# -*- coding: utf-8 -*- 
# AUTHOR: Zeray Rice <fanzeyi1994@gmail.com>
# FILE: create_config.py
# CREATED: 18:55:53 06/04/2012
# MODIFIED: 19:05:15 06/04/2012

import uuid
import getpass
import binascii
from werkzeug.security import generate_password_hash

def input_with_default(prompt, default, pwd = False):
    if pwd:
        x = getpass.getpass("%s (%s): " % (prompt, default))
    else:
        x = raw_input("%s (%s): "%(prompt, default))
    if not x:
        return default
    return x

with open("settings.py", "w") as st:
    print "Generate a config file for Wobbuffet.."
    st.write("# -*- coding: utf-8\n")
    st.write("ADMIN_USERNAME = '''%s'''\n" % input_with_default("Username", "admin"))
    st.write("ADMIN_PASSWORD = '''%s'''\n" % generate_password_hash(input_with_default("Password", "password", pwd = True)))
    st.write("SITE_TITLE = '''%s'''\n" % input_with_default("Site Title", "Wobbuffet"))
    st.write("SQLALCHEMY_DATABASE_URI = '''%s'''\n" % input_with_default("Database URI", "sqlite:///wobbuffet.db"))
    st.write("AUTH = '''%s'''\n" % binascii.b2a_hex(uuid.uuid4().bytes))
    st.flush()

print "Config file created successfully!"
