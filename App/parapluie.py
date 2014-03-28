#!/usr/local/bin/python3

class PyPipeline:
    def run(self, options):
        import core.scriptgenerator
        import core.scriptrunner

        script_generator = core.scriptgenerator.ScriptGenerator(options)
        scripts = script_generator.generate()

        script_runner = core.scriptrunner.ParallelScriptRunner(scripts, int(options['numproc']))                                                               
        script_runner.run()

def parse_args(argv):
    import subprocess
    numproc = int(subprocess.check_output(['sysctl', '-n', 'hw.physicalcpu']))

    import os
    args = {'numproc': numproc,
            'input': '../Input',
            'output': '../Output',
            'pipeline': 'denovota',
            'query': 'Callorhinchus_milii'}

    user_args = dict(i.split('=') for i in argv[1:] if i.find('=') > 0)

    for key in user_args:
        if key in args:
            args[key] = user_args[key]
        else:
            print('Unknown argument:',key)            

    args['input'] = os.path.abspath(args['input'])
    args['output'] = os.path.abspath(args['output'])

    return args

if __name__ == '__main__':
    import sys
    args = parse_args(sys.argv)
    PyPipeline().run(args)
