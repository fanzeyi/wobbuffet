# -*- coding: utf-8 -*- 
# AUTHOR: Zeray Rice <fanzeyi1994@gmail.com>
# FILE: gen_auth.py
# CREATED: 17:20:40 06/04/2012
# MODIFIED: 17:22:10 06/04/2012

import uuid
import binascii

print binascii.b2a_hex(uuid.uuid4().bytes)
