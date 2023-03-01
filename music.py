from nikola.plugin_categories import Task
from nikola import utils
import os


class Music(Task):
	"""Build pages for music tracks"""

	name = "music"

	def gen_tasks(self):
		"""Generate tasks for building music pages."""
		kw = {            
			"blog_url": self.site.config['SITE_URL'],
			"music_folder": "files\\music",
			"output_folder": self.site.config['OUTPUT_FOLDER']
		}
		if not os.path.isdir(os.path.join(kw["output_folder"],"music")): os.mkdir(os.path.join(kw["output_folder"],"music"))
		# Create a task for each language
		lang="en"
		music_path = os.path.join(kw["music_folder"])
		if not os.path.isdir(music_path):
			return print("music path is not valid")

		# Get a list of all music files
		music_files = [f for f in os.listdir(music_path) if f.endswith(".mp3") or f.endswith(".wav") or f.endswith(".flac")]

		# Create a task for each music file
		for music_file in music_files:
			slug = utils.slugify(os.path.splitext(music_file)[0])
			output_name = os.path.join(kw["output_folder"], "music", slug + ".html")
			task_dep = ["render_posts"]
			targets = [output_name]

			def task():
				print(f'music_file: {music_file} \n  output_name: {output_name}')
				self.site.scan_posts()
				deps =[]
				return {
					"basename": self.name,
					"name": output_name,
					"file_dep": deps,
					"targets": targets,
					"actions": [(self.render_music_page, [music_file, self.site.config['SITE_URL'], output_name, lang], {'targets': [output_name], 'file_dep': [music_file]})],
					"clean": True,
					"uptodate": [utils.config_changed(kw, "nikola.plugins.task.music")],
					"task_dep": task_dep,
					"verbosity": 2,
				}

			yield task()

	def render_music_page(self, music_file, site_url, output_name, lang, targets, file_dep):
		"""Render the HTML page for a music track."""
		print(f'music_file: {music_file} \n output_name: {output_name}')
		kw = {
			"title": os.path.splitext(music_file)[0],
			"description": "",
			"dllink": music_file,
			"lang": "en",
			"slug": utils.slugify(os.path.splitext(music_file)[0])
		}
		# Render the page using the appropriate renderer function
		output = self.site.render_template('music.tpl', None,kw)
		with open(output_name, "wb") as output_file:
			output_file.write(output.encode("utf8"))
		return {'targets': [output_name], 'file_dep': [music_file]}