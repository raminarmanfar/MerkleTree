import os

class utilities:
    '''
    HEADER = ''
    OKBLUE = ''
    OKGREEN = ''
    WARNING = ''
    FAIL = ''
    ENDC = ''
    BOLD = ''
    UNDERLINE = '\033[4m'
    '''

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ''''''
    @staticmethod
    def clearScreen():
        os.system('cls' if os.name == 'nt' else 'clear')
        
    @staticmethod
    def getScreenSize():
        ts = os.get_terminal_size()
        return ts
    
    @staticmethod
    def locatePrint(x, y, text, color = ENDC):
        sys.stdout.write(color + "\x1b7\x1b[%d;%df%s\x1b8" % (x, y, text) + disp.ENDC)
        sys.stdout.flush()
