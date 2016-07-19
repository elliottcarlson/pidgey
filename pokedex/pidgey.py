from __future__ import unicode_literals
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import confirm
from termcolor import colored
from cmd2 import Cmd
import sys, time, threading, yaml, json


from .cmd import Cmd
from .account import Account
from .geo import Geo
from .utils import *


class Pidgey(Account, Geo, Cmd):

    username = None
    currency = dict()

    def __init__(self, API):
        #Cmd.__init__(self)
        super(Pidgey, self).__init__()

        self.prompt = colored('>> ', 'white', attrs=['bold'])
        self.api = API

        intro()

        self.get_location()


    def do_inventory(self, line):
        response_dict = self.api.get_inventory().call()
        print('Response dictionary: \n\r{}'.format(json.dumps(response_dict, indent=2)))

    def do_run(self, line):
        def func_not_found():
            print "No Function " + line + " Found!"
        func = getattr(self.api, line, func_not_found)
        func()

    def set_prompt(self):
        self.prompt = ''.join([
            red('{}'.format(self.username if self.username else ''), attrs=['bold']),
            white('>> ')
        ])


    def _config(self):
        "Configure Pidgey"

        credentials = {}
        try:
            credentials = load_config('config/credentials.yaml')
        except:
            pass

        # Prompt for user credentials
        service = service_prompt()

        if service == 'ptc':
            service_name = 'Pokemon Trainer Club'
        else:
            service_name = 'Google'

        username = prompt('Please enter your %s username: ' % service_name)
        password = prompt('Please enter your %s password: ' % service_name,
            is_password=True)

        credentials[service] = dict(
            username = username,
            password = password
        )

        # Save credentials to yaml
        with open('config/credentials.yaml', 'w') as yaml_file:
            yaml_file.write(yaml.dump(credentials, default_flow_style=False))

        return credentials


    def do_config(self, line):
        "Configure Pidgey"

        credentials = self._config()


    def precmd(self, line):
        self.api.set_position(
            self.location['latitude'],
            self.location['longitude'],
            self.location['altitude']
        )
        return Cmd.precmd(self, line)


    def postcmd(self, stop, line):
        self.set_prompt()
        return Cmd.postcmd(self, stop, line)


    def cmdloop(self):
        try:
            Cmd.cmdloop(self)
        except KeyboardInterrupt as e:
            self.__key_interrupt = self.__key_interrupt + 1
            if self.__key_interrupt > 1:
                print('^C')
                self.do_exit(self)
            else:
                print('Press Ctrl-C again to exit.')
                self.cmdloop()
