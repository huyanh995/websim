import requests
from common import utils


alpha_ids = ['3gv8AXP',
'8gWee0X',
'deJx60J',
'derrLoJ',
'EoP9xdJ',
'EoPxoGG',
'JRaq0ql',
'meWW911',
'NklYOVw',
'OKdZXgp',
'QmR3Z0K',
'QmRPmQp',
'WKrPAXZ',
'zX7qXW8',
'zXneXN1'
]




sess = requests.session()
utils.login(sess)
utils.change_name('WKrPAXZ',sess)