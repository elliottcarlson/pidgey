from cmd2 import Cmd as Cmd2

class Cmd(Cmd2, object):
    """
    Wrap Cmd to enable new-style inheritence which is not possible with cmd2 as
    it is an old-style class. Defintetly hax. Must be included as last inherited
    class for this to work.
    """
    def __init__(self):
        Cmd2.__init__(self)


