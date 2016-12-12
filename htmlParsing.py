from HTMLParser import HTMLParser

class FormDefaultParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.form_defaults_map = {}
		self.prev_select = None

	def handle_starttag(self, tag, attrs):
		if tag == "select":
			for attr in attrs:
				if attr[0] == 'name':
					self.prev_select = attr[1]
		elif tag == "option" and self.prev_select is not None:
			selected = False
			value = None
			for attr in attrs:
				if attr[0] == 'value':
					value = attr[1]
				elif attr[0] == 'selected':
					selected = True
			if selected:
				self.form_defaults_map[self.prev_select] = value
		elif tag == "input":
			name = None
			value = None
			checked = False
			f_type = None
			for attr in attrs:
				if attr[0] == 'name':
					name = attr[1]
				elif attr[0] == 'value':
					value = attr[1]
				elif attr[0] == 'type':
					f_type = attr[1]
				elif attr[0] == 'checked':
					checked = True
			if f_type == 'checkbox' and not checked:
				return # don't add the value if the checkbox is not selected
			if name is not None and value is not None:
				self.form_defaults_map[name] = value
