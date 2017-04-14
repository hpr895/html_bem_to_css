import sublime
import sublime_plugin

import ctypes
import re

# from pprint import pprint


class html_bem_to_cssCommand(sublime_plugin.TextCommand):
	def run(self, edit):


		# Часть 1

		# Берём текст из буфера обмера
		def getClipboardText():
			CF_UNICODETEXT = 13
			d = ctypes.windll
			d.user32.OpenClipboard(0)
			handle = d.user32.GetClipboardData(CF_UNICODETEXT)
			data = ctypes.c_wchar_p(handle).value
			d.user32.CloseClipboard()
			return data

		# Всё в одну строку
		def cleanHtml(array):
			full_string = ''
			for line in array:
				line = re.sub('\n', '', line)
				line = re.sub('\r', '', line)
				full_string += line
			return full_string

		# Получаем список классов
		def removeAllWithoutClass(string):
			array = re.findall(r'<.*?class="(.*?)".*?>', string)
			full_string = ''
			for line in array:
				full_string += line + ' '
			new_array = full_string.split(' ')
			return new_array

		# Оставляем только уникальные строки
		def remainUnique(array):
			seen = []
			new_array = []
			for line in array:
				if re.match('\r', line):
					new_array.append(line)
					seen = []
				else:
					if line in seen:
						continue
					seen.append(line)
					new_array.append(line)
			return new_array


		# Часть 2

		# Поднять элементы к блокам
		def sortingElemToBlock(array):
			new_array = []
			for line in array:
				new_array.append(line)
				if '_' not in line:
					new_array.append(line)
					isElem = line + '__'
					for line in array:
						if re.match(isElem, line):
							new_array.append(line)
			return new_array

		# Поднять модификаторы к элементам
		def sortingModToElem(array):
			new_array = []
			for line in array:
				new_array.append(line)
				if '__' in line and '[a-zA-Z0-9]_[a-zA-Z0-9]' not in line:
					new_array.append(line)
					isMod = line + '_'
					for line in array:
						if re.match(isMod, line):
							new_array.append(line)
			return new_array

		# Поднять модификаторы к блокам
		def sortingModToBlock(array):
			new_array = []
			for line in array:
				new_array.append(line)
				if '_' not in line:
					new_array.append(line)
					isMod = line + '_'
					for line in array:
						if re.match(isMod, line) and '__' not in line:
							new_array.append(line)
			return new_array


		# Часть 3

		# Конвертируем всё в CSS разметку
		def convertToCSS(array):
			new_array = []
			for line in array:
				if line.strip():
					line = '.' + line + ' {\n    \n}\n'
					new_array.append(line)
			return new_array


		# Заключение

		# Вставляем в Sublime Text результат
		def SublimeInsertText(array):
			for line in array:
				pos = self.view.sel()[0].begin()
				self.view.insert(edit, pos, line + '\n')

		# Финальное объединение всего плагина
		def makeFinal():
			fin = getClipboardText()
			fin = cleanHtml(fin)
			if fin:
				fin = removeAllWithoutClass(fin)
				fin = sortingElemToBlock(fin)
				fin = remainUnique(fin)
				fin = sortingModToElem(fin)
				fin = remainUnique(fin)
				fin = sortingModToBlock(fin)
				fin = remainUnique(fin)
				fin = convertToCSS(fin)
				sublime.status_message('HTML to CSS: Conversion was successful')
			else:
				sublime.status_message('HTML to CSS: Error - array has no length')
			SublimeInsertText(fin)
		makeFinal()


