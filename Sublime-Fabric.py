# Fabric.py
# Sublime-Fabric excute task Fabric for Sublime Text 2
#
# Project: https://github.com/b3ni/Sublime-Fabric
# License: MIT

import sublime
import sublime_plugin
import os


class FabTasks(sublime_plugin.WindowCommand):
    """Fabric using repl in st2"""
    def run(self):
        for folder in self.window.folders():
            self._fabfiles = filter(len, subprocess.Popen(
                ['find', folder, '-name', 'fabfile.py'],
                stdout=subprocess.PIPE,
            ).stdout.read().split('\n'))
        self.files, self.tasks = zip(*reduce(
            lambda values, file: values + map(
                lambda task: (file, task), filter(
                    len, subprocess.Popen([
                        'fab', '-l', '-F', 'short', '-f', file
                    ], stdout=subprocess.PIPE).stdout.read().split('\n'),
                ),
            ), self._fabfiles, [],
        ))
        self.window.show_quick_panel(
            list(self.tasks), self.execute,
            sublime.MONOSPACE_FONT,
        )

    def execute(self, index):
        if index != -1:
            task = self.tasks[index]
            path = self.files[index]
            self.window.run_command("repl_open", {
                "type": "subprocess",
                "encoding": "utf8",
                "suppress_echo": True,
                "cmd": ['fab', task, '-f', path],
                'cwd': os.path.dirname(path),
            })
