import os
import sys

class Utils:
    def __init__(self):
        pass
    
    @staticmethod
    def resourcePath(relative_path):
        if getattr(sys, 'frozen', False):
            base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
            return os.path.join(base_path, relative_path)
        else:
            return relative_path