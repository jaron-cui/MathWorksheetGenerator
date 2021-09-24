import os

# LaTeX Interfacing Classes
#   by Jaron Cui
#   8/17/2021

# This file contains classes for interfacing with common features of LaTeX.
# Documents can be exported as .tex and .pdf.
# (As long as your computer knows how to compile .tex to .pdf automatically)


# Generic document class with minimal packages
class Document(object):
  # Constructor
  def __init__(self):
    self.preamble = set()
    self.margin = 1
    self.elements = []
    self.usepackage("{fancyhdr}")

  # Adds some text to the technical preamble
  def add_to_preamble(self, text):
    for line in str.split(text, "\n"):
      self.preamble.add(line)

  # Adds a \usepackage statement to the preamble to import a package
  def usepackage(self, package):
    self.add_to_preamble("\\usepackage" + package)

  # Sets the margin of the document
  def set_margin(self, amount):
    self.usepackage("[margin=" + amount + "]{geometry}")

  # Adds a document element
  def add_element(self, element):
    self.elements.append(element)

  # Adds raw LaTeX script to the document
  def add_raw(self, text):
    self.add_element(Text(text))

  # Exports the document as a .tex and .pdf
  def export(self, name):
    filename = name + ".tex"
    out = open(filename, "w")
    def writelines(lines):
      newlines = []
      for line in lines:
        newlines.append(line + "\n")
      out.writelines(newlines)

    out.write("\\documentclass{article}\n")
    writelines(self.preamble)

    out.write("\\begin{document}\n")
    for element in self.elements:
      print(type(element.get_lines()))
      writelines(element.get_lines())
    out.write("\\end{document}\n")

    out.close()
    os.system("pdflatex " + filename)


# Represents a document with additional presets used often for academic worksheets
class AcademicDocument(Document):
  def __init__(self):
    super().__init__()
    self.set_margin("1in")
    self.usepackage("[english]{babel}")
    self.usepackage("[utf8]{inputenc}")
    self.usepackage("{array}")
    self.usepackage("{rotating}")


# DOCUMENT ELEMENTS

# A textual document element
class Text:
  def __init__(self, text):
    if isinstance(text, str):
      self.lines = str.split(text, "\n")
    else:
      self.lines = text

  # Adds a line of text to the element
  def add_line(self, line):
    self.lines.append(line)

  # Returns a list of text lines
  def get_lines(self):
    return self.lines


# A document element that ends the current page and starts a new one
class NewPage(Text):
  def __init__(self):
    super().__init__("\\newpage")


# A document element that begins a new section
class Section(Text):
  def __init__(self, name):
    super().__init__("\\section*{" + name + "}")


# A generic bounded element in LaTeX (i.e. uses \begin and \end)
class BoundedElement(Text):
  def __init__(self, name, parameters, *args):
    contents = Text("") if len(args) == 0 else args[0]
    super().__init__(contents.get_lines())
    self.begin = "\\begin{" + name + "}" + parameters
    self.end = "\\end{" + name + "}"

  # Wraps the lines in the appropriate \begin and \end statements
  def get_lines(self):
    return [self.begin] + Text.get_lines(self) + [self.end]


# A document element that aligns its contents to the left
class FlushLeft(BoundedElement):
  def __init__(self, contents):
    super().__init__("flushleft", "", contents)


# A document element that centers its contents
class Center(BoundedElement):
  def __init__(self, contents):
    super().__init__("center", "", contents)


# A document element that aligns its contents to the right
class FlushRight(BoundedElement):
  def __init__(self, contents):
    super().__init__("flushright", "", contents)


# A document element that creates a configurable table
class Table(BoundedElement):
  def __init__(self, column_count, column_width, row_spacing, outlined):
    spacer = "|" if outlined else " "
    config = spacer
    for n in range(column_count):
      config += "m{" + column_width + "}" + spacer
    config = "{" + config + "}"

    super().__init__("tabular", config)
    self.column_count = column_count
    self.row_spacing = row_spacing

  # Sets the spacing between rows
  def set_row_spacing(self, spacing):
    self.row_spacing = spacing

  # Sets the document elements contained in the table
  def set_items(self, items):
    def last_in_column(n):
      return n % self.column_count == self.column_count - 1

    self.lines = []
    for n in range(len(items)):
      item = items[n]
      self.lines += item.get_lines()
      self.lines.append(" \\\\[" + self.row_spacing + "]" \
        if last_in_column(n) else " & ")


# A document element that sets the style of the current page
class SetStyle(Text):
  def __init__(self):
    super().__init__("")

  def set_type(self, style_type):
    self.add_line("\\pagestyle" + style_type)

  def get_lines(self):
    unique_id = str(self.__hash__())
    return ["\\fancypagestyle{" + unique_id + "}{"] + Text.get_lines(self) \
            + ["}\\thispagestyle{" + unique_id + "}"]


# A document element that disables page numbers
class PageNumbersOff(Text):
  def __init__(self):
    super().__init__("\\pagenumbering{gobble}")