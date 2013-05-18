import os
import sys

from core.script import Script

class ScriptGenerator(object):
    def __init__(self, options):
        self.input_directory = '../Input'
        self.temporary_directory = options['temporary_directory']

    def generate(self):
        files = self.find_files(self.input_directory, '.fastq')
        files += self.find_files(self.input_directory, '_001.fastq')

        scripts = []
        
        for file in files:
            root = file.split(os.sep)[-1]

            directory = self.temporary_directory + os.sep + root

            script = Script(root, directory)
            
            if sys.version_info < (3, 0):
                pipeline = raw_input('Pipeline for "' + root + '"?: ')
            else:
                pipeline = input('Pipeline for "' + root + '"?: ')

            script.load_pipeline(pipeline)
            scripts.append(script)

        return scripts

    def find_files(self, directory, suffix):
        all_files = os.listdir(directory)
        files = [f[:-len('_R1' + suffix)] for f in all_files]

        return list(set([f for f in files if f + '_R2' + suffix in all_files]))
