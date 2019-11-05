#from lark import Lark
from syntax.parse import Lark_StandAlone, LarkError
from colorclass import Color
import readline

#parser = Lark.open(
#  'syntax/apparat.lark',
#  rel_to=__file__,
#  debug=True,
#  parser='lalr',
#  start='root',
#)

def main():
  parser = Lark_StandAlone()

  print("Apparat rev. 0. 1")

  while True:
    source = input(Color('{autogreen}~{/green} '))
    count = source.count

    while [count('{'), count('('), count('[')] != [count('}'), count(')'), count(']')]:
      source += '\n' +  input('... ')
      count = source.count

    try:
      ast = parser.parse(source).pretty()
      print(ast)
    except LarkError as err:
      head = Color('{autored}=== SORRY! ==={/red}')
      print(f'\033[1;m{head}\033[0m\n Syntax error caused by \'{source[err.pos_in_stream]}\'',
            f'at line {err.line}, column {err.column} (of <stdin>)\n')

if __name__ == '__main__':
  main()
