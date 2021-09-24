import math
import random
import latex_interfacing as latex

# Math Worksheet Generator
#   by Jaron Cui
#   8/17/2021

# My younger sister needed math practice. However, you see, she did not
# particularly desire math practice. So, when I completed this worksheet generator,
# you may be able to correctly infer that she was not particularly thrilled.


# Worksheet elements
header = latex.SetStyle()
header.set_type("{fancy}")
header.add_line("\\lhead{Date: \\underline{\\hspace{3cm}}}")
header.add_line("\\chead{Time: \\underline{\\hspace{3cm}}}")
header.add_line("\\rhead{Score: \\underline{\\hspace{4cm}}}")

prompt = latex.Text("Solve as many of the problems below as you can in the allotted time. "
                    "If the problem expression contains only whole numbers, "
                    "your answer should be a whole number. "
                    "If the problem expression contains decimals, "
                    "your answer should too.\\bigskip\\bigskip\\\\")

questions = latex.Table(4, "4cm", "3.5cm", False)
answer_key = latex.Table(4, "4cm", "10pt", False)


# Randomizes and exports a practice math worksheet into the project folder
def make_sheet(name, problem_gen):
  # Random problem and answer generation
  prompts = []
  answers = []
  for n in range(1, 21):
    problem = problem_gen()
    prompts.append(latex.Text(str(n) + ". $" + problem["prompt"] + "$"))
    answers.append(latex.Text(str(n) + ". $" + problem["answer"] + "$"))

  # Placing generated prompts and answer text into LaTeX interfacing classes
  questions.set_items(prompts)
  answer_key.set_items(answers)

  # Front page setup (question side)
  doc = latex.AcademicDocument()
  doc.add_element(latex.PageNumbersOff())
  doc.add_element(header)
  doc.add_element(latex.Section("Timed Math Practice Sheet"))
  doc.add_element(prompt)
  doc.add_element(questions)

  # Back page setup (answer key side)
  doc.add_element(latex.NewPage())
  doc.add_element(latex.Text("\\vspace*{\\fill}"))
  doc.add_element(latex.FlushRight(latex.BoundedElement("turn", "{180}", answer_key)))

  # Export as .tex and .pdf
  doc.export(name)


# Generates a random integer on the interval [_low_, _high)
def random_int(low, high):
  return math.floor(random.random() * (high - low) + low)


# Generates a random decimal on the interval [_low_, _high)
# with a specified maximum number of places past the decimal point
def random_dec(low, high, precision):
  scale = math.pow(10, random_int(1, precision + 1))
  return random_int(low * scale, high * scale) / scale


# Generates an integer multiplication problem formatted as
# a dict {"prompt": ..., "answer": ...}
def random_int_multiplication(low, high):
  def generator():
    a = random_int(low, high)
    b = random_int(low, high)
    text = str(a) + " \\times " + str(b) + " ="
    answer = str(a * b)
    return {"prompt": text, "answer": answer}

  return generator


# Generates a decimal multiplication problem formatted as
# a dict {"prompt": ..., "answer": ...}
def random_dec_multiplication(low, high, precision):
  def generator():
    a = random_dec(low, high, precision)
    b = random_dec(low, high, precision)
    text = str(a) + " \\times " + str(b) + " ="
    answer = str(round(a * b, 2 * precision))
    return {"prompt": text, "answer": answer}

  return generator


# Generates an integer division problem formatted as
# a dict {"prompt": ..., "answer": ...}
def random_int_division(low, high):
  def generator():
    a = random_int(low, high)
    b = random_int(low, high // 10)
    text = str(a) + " \\div " + str(b) + " ="
    answer = str(a // b) + "r" + str(a % b)
    return {"prompt": text, "answer": answer}

  return generator


# Generates a decimal division problem formatted as
# a dict {"prompt": ..., "answer": ...}
def random_dec_division(low, high, precision):
  def generator():
    a = random_dec(low, high // 10, precision)
    ans = random_dec(min(high // a, low), max(high // a, low), precision)
    b = round(a * ans, 2 * precision)
    text = str(b) + " \\div " + str(a) + " ="
    answer = str(ans)
    return {"prompt": text, "answer": answer}

  return generator


# Further randomizes problem generation by taking in a list of
# problem generators and returning a function that, when called,
# returns the result of a call on a randomly selected generator
def random_problem(generators):
  def generator():
    return generators[random_int(0, len(generators))]()

  return generator

# WORKSHEET GENERATION AND EXPORT
make_sheet("example_worksheet", random_problem([random_int_multiplication(1, 1000),
                                                random_dec_multiplication(1, 100, 1),
                                                random_dec_multiplication(1, 10, 2),
                                                random_int_division(1, 1000),
                                                random_dec_division(1, 1000, 1)]))