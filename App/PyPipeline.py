#!/usr/local/bin/python3

class PyPipeline:
    def run(self, num_cores, use_gui=False):
        import core.temp
        import core.scriptgenerator
        import core.scriptrunner
        import gui.options

        options = {'temporary_directory' : '../Output/Intermediate/'}

        if use_gui:
            options = gui.options.OptionsWindow(scripts).get_options()
        else:
            options['input_directory'] = '../Input'

        script_generator = core.scriptgenerator.ScriptGenerator(options)
        scripts = script_generator.generate()

        script_runner = core.scriptrunner.ParallelScriptRunner(scripts, num_cores)

        print('Using options:', options)

        if use_gui:
            gui.viewer.ScriptRunnerViewer(script_runner).start()
        else:
            script_runner.run()

if __name__ == '__main__':
    PyPipeline().run(1, False)
