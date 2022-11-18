from typing import List, Optional, Any
import re
from dataclasses import dataclass

file_path = "/Users/bzy/Desktop/2sph-cylinder.k"

@dataclass
class CONTROL_SPH:
	__tag_name = "control_sph"
	__name = "CONTROL_SPH"

	start_line: int = 0

	ncbs: str = ""
	boxid: str = ""
	dt: str = ""
	idim: str = ""
	nmneigh: str = ""
	form: str = ""
	start: str = ""
	maxv: str = ""

	@property
	def tag_name(self):
		return self.__tag_name

	def __eq__(self, content: str) -> bool:
		return self.__name in content

@dataclass
class KeyFileParser:
	_cur_idx: int = 0
	lines: List[str] = None

	control_sph: CONTROL_SPH = None

	@property
	def cur_line(self):
		return self.lines[self._cur_idx]

	@property
	def parse_end(self):
		return self._cur_idx == len(self.lines) - 1

	@property
	def is_title(self):
		return self.lines[self._cur_idx].startswith("$#")

	@property
	def is_tag(self):
		return self.lines[self._cur_idx].startswith("*")

	@property
	def is_value(self):
		return not(self.is_tag or self.is_title)

	@property
	def tag(self) -> Any:
		if self.lines[self._cur_idx] == CONTROL_SPH():
			return CONTROL_SPH(
				start_line=self._cur_idx + 1
			)
		return None

	def idx_add(self):
		self._cur_idx += 1

	def parse_line(self):
		start = 0
		step = 10
		values = []
		line = self.cur_line.replace("$#", "  ")
		while True:
			end = start + step
			value = line[start: start + step]
			if not value:
				break

			if value.strip()!= '':
				values.append(value.strip())
			start = end

		return values

	def parse_params(self):
		while True:
			if self.parse_end:
				self._cur_idx == 0
				break

			self.parse()
			self.idx_add()

	def parse(self):
		if not self.tag:
			return
		tag = self.tag
		keys, values = [], []
		while True:
			self.idx_add()
			if self.is_tag:
				break
			elif self.is_title:
				keys.extend(self.parse_line())
			elif self.is_value:
				values.extend(self.parse_line())

		attr_dict = dict(zip(keys, values))
		tag.__dict__.update(attr_dict)
		setattr(self, tag.tag_name, tag)

with open(file_path, 'r') as key_file:
	file_parser = KeyFileParser(lines=key_file.readlines())
	file_parser.parse_params()