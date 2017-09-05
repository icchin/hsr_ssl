#!/usr/local/bin/python3
import re
import os
from io import BytesIO
from distutils.errors import DistutilsError
from subprocess import check_output

import sys


def simple_call(cmd):
	return check_output(cmd.split(" "))


class IncrementSemanticVersion():
	"""Increment Semantic Version and Commmit to Git
    Version incrementing uses semantic versioning. This command accepts -M or
    --major, -m or --minor to increment a major or minor release. If no flags
    are passed then a patch release is created.
    """

	user_options = [
		("major", "M", "increment version for major release"),
		("minor", "m", "increment version for minor release"),
	]

	boolean_options = ("major", "minor")


	def _new_version(self, version):
		major, minor, patch = [int(i) for i in version.split(".")]

		if self.major:
			return "{}.0.0".format(major + 1)
		elif self.minor:
			return "{}.{}.0".format(major, minor + 1)
		else:
			return "{}.{}.{}".format(major, minor, patch + 1)

	def update_init(self, new_version):
		init_py = "angle/__init__.py"
		lines=open(init_py, "rt").readlines()
		output=open(init_py, "wt")
		for line in lines:
			if "__version__" in line:
				line = '__version__="{}",\n'.format(new_version)
			output.write(line)


	def _update_version(self):
		pattern = re.compile('^(\s+)version="([0-9\.]+)"')
		pattern2 = re.compile('^(\s+)version=\'([0-9\.]+)\'')
		output = BytesIO()
		new_version=None
		with open("setup.py", "rt") as fp:
			for line in fp:
				result = pattern.match(line) or pattern2.match(line)
				if not result:
					output.write(line.encode())
				else:
					spaces, version = result.groups()
					new_version = self._new_version(version)
					output.write('{}version="{}",\n'.format(spaces, new_version).encode())

		if not new_version:
			raise Exception("NO new_version")

		# sys.setdefaultencoding('UTF8')
		with open("setup.py", "wt") as fp:
			# fp.write(str(output.getvalue()))
			fp.write(str(output.getvalue(), 'UTF-8'))
		# output.write(line) # TypeError: a bytes-like object is required, not 'str'
	# fp.write(output)  # TypeError: write() argument must be str, not bytes PYTHON3, YOU FUCKING KIDDING ME???

		return new_version


	def _run(self):
		self.major = False
		self.minor = False
		# if simple_call("git status --porcelain").strip():
		# 	os.system("git commit -a --allow-empty-message -m ''  ")
		# raise DistutilsError("Uncommited changes, commit all changes before release")

		new_version = self._update_version()
		self.update_init(new_version)
		print("new_version "+new_version)
		# self.distribution.metadata.version = new_version
		# os.system("git commit -m Release {}".format(new_version))
		# os.system("git tag release-{}".format(new_version))


IncrementSemanticVersion()._run()
