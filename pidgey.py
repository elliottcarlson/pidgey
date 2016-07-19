#!/usr/bin/env python
from pokedex import Pidgey
from termcolor import colored
import traceback

import sys
sys.path.append('./pgoapi/')
from pgoapi import PGoApi

DEBUG = True

if __name__ == '__main__':
    pidgey = Pidgey(PGoApi())

    try:
        pidgey.cmdloop()
    except Exception as e:
        traceback.print_exc()

        print(colored('[%s] %s' % (colored('ERR', 'red'), str(e)), 'white', attrs['bold']))
        pidgey.cmdloop()
