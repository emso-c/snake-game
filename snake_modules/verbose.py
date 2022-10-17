class Verbose:
    def __init__(self, verbose:bool):
        self.verbose = verbose

    def vprint(self, *args):
        if self.verbose:
            print(*args)