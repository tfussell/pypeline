import os
import os.path
import shutil
import subprocess
import collections
import sys

Message = collections.namedtuple('Message', 'task_name type value')

MESSAGE_INDICATOR = '$+_pypipeline_+$'

class Script(object):
    def __init__(self, name, directory, query, input_directory, output_directory):
        self.name = name
        self.commands = []
        self.working_directory = directory
        self.query = query
        self.input_directory = input_directory
        self.output_directory = input_directory
        
    def execute(self, message_queue):
        outfile = open(self.working_directory + os.sep + self.name + '.log', 'wb')

        process = subprocess.Popen(''.join(self.commands), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, bufsize=1, cwd=self.working_directory)

        while process.poll() == None:
            line = process.stdout.readline().decode()

            if line[:len(MESSAGE_INDICATOR)] == MESSAGE_INDICATOR:
                print(line[len(MESSAGE_INDICATOR) + 1:-1])
            elif line and outfile:
                outfile.write(line.encode('utf-8'))

        outfile.close()

    def template_replace(self, template, template_variables):
        for key in template_variables:
            skey = '{% ' + key + ' %}'
            index = template.find(skey)

            while index >= 0:
                template = template[:index] + template_variables[key] + template[index + len(skey):]
                index = template.find(skey)

        return template

    def query_parameters(self, parameters):
        for key in parameters:
            if not parameters[key]:
                if key == 'query':
                    parameters[key] = self.query
                elif sys.version_info < (3, 0):
                    parameters[key] = raw_input(self.name + ', ' + key + ': ')
                else:
                    parameters[key] = input(self.name + ', ' + key + ': ')

        return parameters

    def load_pipeline(self, pipeline):
        script_template_filename = '..' + os.sep + 'Pipelines' + os.sep + pipeline + os.sep + 'script'
        parameters_filename = '..' + os.sep + 'Pipelines' + os.sep + pipeline + os.sep + 'parameters'
        template_directory = '..' + os.sep + 'Pipelines' + os.sep + pipeline + os.sep + 'template'

        if (not os.path.isfile(script_template_filename) and
            not os.path.isfile(parameters_filename)):
            raise Error('Files "script" and "parameters" not found for the given pipeline')

        script_template_file = open(script_template_filename, 'r')
        template_script = list(script_template_file)
        script_template_file.close()

        parameters_file = open(parameters_filename, 'r')
        template_variables = {line.split()[0] : ' '.join(line.split()[1:]) for line in parameters_file}
        parameters_file.close()

        template_variables = self.query_parameters(template_variables)

        # Special parameters
        template_variables['name'] = self.name
        template_variables['directory'] = self.working_directory
        template_variables['input_directory'] = self.input_directory
        template_variables['output_directory'] = self.output_directory

        self.commands = [self.template_replace(command, template_variables) for command in template_script]
        
        num_commands = len(self.commands)

        for i in range(len(self.commands)):
            self.commands.insert(i * 2, 'echo {} {} {}/{}: "{}"\n'.format(MESSAGE_INDICATOR, self.name, i, num_commands, self.commands[i * 2]))

        if not os.path.isdir(self.working_directory):
            if template_directory and os.path.isdir(template_directory):
                shutil.copytree(template_directory, self.working_directory)
            else:
                os.makedirs(self.working_directory)

