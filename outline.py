
import sublime, sublime_plugin
import re
import sys

class OutlineDump(sublime_plugin.EventListener):

	outline_view = 0
	outline_view_id = 0

	def on_post_save(self, view):
		if self.is_open(self.outline_view_id) == False:
			self.create_view(view)

		self.refresh(view)


	def refresh(self, view):
		self.erase_all(self.outline_view)
		text = view.substr(sublime.Region(0, view.size()))
		results = re.compile(r"(?:protected|public|private|package) (\w+ \w+\([^\)]+\)) {").findall(text)
		for item in results:
			print item
			self.add_line(self.outline_view, item)
	
	def add_line(self, outline_view, line):
		line = line.replace('\n', ' ')
		line = re.sub('\s+', ' ', line)
		outline_view.set_read_only(False)
		edit = outline_view.begin_edit()
		outline_view.insert(edit, outline_view.size(), line + '\n')
		outline_view.end_edit(edit)
		outline_view.set_read_only(True)

	def erase_all(self, outline_view):
		outline_view.set_read_only(False)
		edit = outline_view.begin_edit()
		outline_view.erase(edit, sublime.Region(0, outline_view.size()))
		outline_view.end_edit(edit)
		outline_view.set_read_only(True)

	def is_open(self, id):
		opened = False
		for window in sublime.windows():
			for view in window.views():
				if view.id() == self.outline_view_id:
					opened = True
		return opened

	def create_view(self, view):
		self.outline_view = sublime.Window.new_file(view.window())
		self.outline_view_id = self.outline_view.id()
