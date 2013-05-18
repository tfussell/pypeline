#!/usr/local/bin/python3

class PyPipeline:
    def run(self, num_cores, gui=False):
        import core.temp
        import core.scriptgenerator
        import core.scriptrunner
        import gui.options

        with core.temp.tempdir() as temporary_directory:
            script_generator = core.scriptgenerator.ScriptGenerator({'temporary_directory' : temporary_directory})
            scripts = script_generator.generate()

            if gui:
                options = gui.options.OptionsWindow(scripts).get_options()
            else:
                options = {'input_directory' : '../Input'}

            options['temporary_directory'] = temporary_directory

            script_runner = core.scriptrunner.ParallelScriptRunner(scripts, num_cores)

            if gui:
                gui.viewer.ScriptRunnerViewer(script_runner).start()
            else:
                script_runner.run()

if __name__ == '__main__':
    PyPipeline().run(1, True)
