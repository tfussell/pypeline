import os
import sys

from core.script import Script

class ScriptGenerator(object):
    def __init__(self, options):
        self.input_directory = options['input']
        self.working_directory = options['output'] + os.sep + 'Intermediate'
        self.pipeline = options['pipeline']
        self.query = options['query']
        self.output_directory = options['output']

    def generate(self):
        files = self.find_files(self.input_directory, '.fastq')
        files += self.find_files(self.input_directory, '_001.fastq')

        scripts = []
        
        for file in files:
            root = file.split(os.sep)[-1]

            directory = self.working_directory + os.sep + root

            script = Script(root, directory, self.query, self.input_directory, self.output_directory)
            
            script.load_pipeline(self.pipeline)
            scripts.append(script)

        print('Scripts:', files)

        return scripts

    def find_files(self, directory, suffix):
        all_files = os.listdir(directory)
        files = [f[:-len('_R1' + suffix)] for f in all_files]

        return list(set([f for f in files if f + '_R2' + suffix in all_files]))
