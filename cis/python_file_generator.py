#!/usr/bin/env python3
# File Name: python_file_generator.py
# Author: Justin Smith
# Date: 8/25/17 - 8/28/17
# Purpose: Create files with the header filled in.

import datetime
import os
import sys

AUTHOR = 'Justin Smith'
PURPOSE = 'NEEDS TO BE FILLED IN.'
SHEBANG = '#!/usr/bin/env python3'

BOX_LINE = '#' * 40
DATE_TEMPLATE = "{month}/{day}/{year}"
HEADER_TEMPLATE = """{shebang}
# File Name: {filename}
# Author: {author}
# Date: {date}
{box}
\"\"\"{purpose}\"\"\"
"""

def get_date():
  """ Returns a human readable version of the date formatted like mm-dd-year
:return formatted date string"""
  today = datetime.date.today()
  format_args = {'month': today.month, 'day': today.day, 'year': today.year}
  return DATE_TEMPLATE.format(**format_args)


def generate_header(filename, author=None, purpose=None, shebang=None, box=None):
  """ Generates a header with the supplied values
Args:
  filename \tthe filename of the created python script
  author \t(Justin Smith) the author name to use
  purpose \t(NEEDS TO BE FILLED IN) the purpose of the script
  shebang \t(#!/usr/bin/env python3) the shebang line
:return formatted header with header values"""
  global AUTHOR, PURPOSE, SHEBANG, HEADER_TEMPLATE, BOX_LINE

  # Validating values
  if author is None:
    author = AUTHOR
  if purpose is None:
    purpose = PURPOSE
  if shebang is None:
    shebang = SHEBANG
  if box is None:
    box = False
  date = get_date()

  format_args = {'shebang':shebang, 'author':author, 'purpose': purpose, 
                 'date': date, 'filename': filename}
  if box:
    format_args['box'] = BOX_LINE + '\n'
  else:
    format_args['box'] = ''

  return HEADER_TEMPLATE.format(**format_args)


def create_file(filename=None, author=None, purpose=None, shebang=None, add_box=None):
  """Creates the python file with the formatted header.
Args:
  filename \t(testing.py) the filename of the created python script
  author \t(Justin Smith) the author name to use
  purpose \t(NEEDS TO BE FILLED IN) the purpose of the script
  shebang \t(#!/usr/bin/env python3) the shebang line
:returns if file was created successfully"""
  global BOX_LINE

  if add_box is None:
    add_box = False

  if filename is None:
    filename = 'testing'

  if not filename.endswith('.py'):
    filename = '{}.py'.format(filename)

  header = generate_header(filename, author=author, purpose=purpose,
                             shebang=shebang)
  if add_box:
    header = '{}{}'.format(header, BOX_LINE)
    
  try:
    with open(filename, 'w+') as new_file:
      new_file.write(header)
    return True
  except IOError as e:
    print(e)
    return False


def main():
  """ The main method that is executed when the script is run.
Command line options:
 -a, \tAuthor's name in the header.
 -b, \tAdds a line of hashes at the end of the header.
 -f, \tDeletes the file after creating it.
 -p, \tPurpose in the header.
Example usage: python python_file_generator.py -a "Justin Smith" <filename>(.py)
Tip: You can use quotes in order to put spaces in an argument."""
  global AUTHOR, PURPOSE, SHEBANG, HEADER_TEMPLATE
  if len(sys.argv) < 2:
    print('Missing filename.')
  elif '-h' in sys.argv or '--help' in sys.argv:
    print(main.__doc__)
  else:
    # Initalization
    author_flag = -1
    box_flag = -1
    faking_flag = -1
    purpose_flag = -1

    sys.argv = sys.argv[1:]
    print(sys.argv)

    real_author_name = AUTHOR
    real_purpose = PURPOSE

    # Flag handling
    try:
      author_flag = sys.argv.index('-a')
    except ValueError:
      #Author flag wasn't found.
      pass
    try:
      box_flag = sys.argv.index('-b')
    except ValueError:
      #Box flag wasn't found
      pass
    try:
      faking_flag = sys.argv.index('-f')
    except ValueError:
      #Faking flag wasn't found
      pass
    try:
      purpose_flag = sys.argv.index('-p')
    except ValueError:
      #Purpose flag wasn't found.
      pass

    if box_flag > -1:
      sys.argv.remove('-b')

    if author_flag > -1:
      sys.argv.pop(author_flag)
      # This should pop the value of the argument
      real_author_name = sys.argv.pop(author_flag)

    if purpose_flag > -1:
      real_purpose = sys.argv[purpose_flag + 1]
      
    if len(sys.argv) == 0:
      raise ValueError('No filename found!')

    file_name = sys.argv[-1]
    if not file_name.endswith('.py'):
      file_name += '.py'

    b_box_flag = True if box_flag > -1 else False
    success = create_file(file_name, author=real_author_name, purpose=real_purpose, add_box=b_box_flag)
    if success:
      print('File {} made!'.format(file_name))
    else:
      print('There may be an error!')

    if faking_flag > -1:
      os.remove(file_name)
      print('File {} cleaned up!'.format(file_name))


def test_main():
  print(BOX_LINE)

if __name__ == '__main__':
  #test_main()
  main()
