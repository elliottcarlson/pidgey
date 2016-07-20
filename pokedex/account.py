from __future__ import unicode_literals
from prompt_toolkit import prompt
from utils import *
import json

class Account(object):
    def __init__(self):
        super(Account, self).__init__()


    def do_accounts(self, line):
        ret = self.__accounts()


    def do_login(self, line):
        "Login to Pokemon Go"
        try:
            credentials = load_config('config/credentials.yaml')
        except IOError:
            print('No accounts configured; please create one now.')
            credentials = self.__accounts()

        if (len(credentials.keys())) > 1:
            print('More than one account configured; please select one:')
            key = self.select(list(credentials.keys()))
            account = credentials.get(key, {})
        else:
            account = credentials.itervalues().next()

        if not self.api.login(account.get('service', None),
            account.get('username', None), account.get('password', None)):
            raise Exception('Unable to login to your account.')

        player = self.api.get_player().call()

        profile = player['responses']['GET_PLAYER']['profile']
        self.username = profile['username']

        print(white('Welcome back {}!'.format(red(self.username))))


    def __accounts(self):
        try:
            credentials = load_config('config/credentials.yaml')
        except IOError:
            credentials = {}

        account = dict()
        action = None
        actions = [ 'Add New Account' ]
        if len(credentials.keys()) > 0:
            print('Select an account to edit:')
            actions[:0] = sorted([ '%s' % alias for alias in
                list(credentials.keys()) ])
            action = self.select(actions)

            if action != 'Add New Account':
                account = dict(credentials.pop(action, None))

        print('Select the authentication service for this account:')
        selected = account.get('service', None)
        services = [
            'PTC {}'.format(' (Selected)' if selected == 'ptc' else ''),
            'Google {}'.format(' (Selected)' if selected == 'google' else '')
        ]
        service = self.select(services).partition(' ')[0]

        username = prompt('Please enter your {} username: '.format(service),
                default='{}'.format(account.get('username', '')))
        password = prompt('Please enter your {} password: '.format(service),
            is_password=True, default='{}'.format(account.get('password', '')))
        alias = prompt('Please enter an alias for this account: ',
                default='{}'.format(action if action else ''))

        credentials.update({
            alias: {
                'service': service.lower(),
                'username': username,
                'password': password
            }
        })

        with open(os.path.realpath('config/credentials.yaml'), 'w') as yaml_file:
            yaml_file.write(yaml.safe_dump(credentials, default_flow_style=False))

        return credentials
