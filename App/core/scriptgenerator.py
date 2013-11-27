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
        if not files:
            files = self.find_files(self.input_directory, '_001.fastq')

        scripts = []
        
        for file in files:
            root = file.split(os.sep)[-1]

            directory = self.working_directory + os.sep + root
            script = Script(root, directory, self.query, self.input_directory, self.output_directory)
            
            pipeline = self.pipeline
 
            if self.pipeline == 'denovota':
                read_length = self.find_read_length(self.input_directory + os.sep + file)
                if read_length == 150:
                    pipeline = 'denovota150'
                else:
                    pipeline = 'denovota250'

                print('Detected read length', read_length, 'for input', root) 

            script.load_pipeline(pipeline)
            scripts.append(script)

        return scripts

    def find_read_length(self, filename):
        if os.path.isfile(filename + '_R1.fastq'):
            filename += '_R1.fastq'
        elif os.path.isfile(filename + '_R1_001.fastq'):
            filename += '_R1_001.fastq'
        file = open(filename, 'r')
        file.readline()
        return len(file.readline().strip()) - 1

    def find_files(self, directory, suffix):
        if not os.path.isdir(directory):
            print('Error - Invalid input directory: ' + directory)
            sys.exit(1)

        all_files = os.listdir(directory)
        files = [f[:-len('_R1' + suffix)] for f in all_files]

        return list(set([f for f in files if f + '_R2' + suffix in all_files]))
