from syntax.parse import Lark_StandAlone, LarkError
from colorclass import Color
import readline

def error(message):
  head = Color('{autored}=== SORRY! ==={/red}')
  print(f'\033[1;m{head}\033[0m\n{message}\n')

def parse(parser, source, filename = 'in'):
  try:
    return True, parser.parse(source)
  except LarkError as err:
    cause = source[err.pos_in_stream]

    error(f'Syntax error caused by \'{cause}\' ' \
          f'at line {err.line}, column {err.column} (of <{filename}>)')

    return False, ()

def main(argv):
  parser = Lark_StandAlone()

  justParse, enableRepl = False, True

  try:
    for arg in argv:
      if arg in ['-ast', '-a']:
        justParse = True
      elif arg in ['-bytes', '-b']:
        raise NotImplementedError('Bytecode generation not implemented yet')
      elif arg in ['-help', '-h']:
        enableRepl = False # so we exit right after we print

        print ('Usage:\n apparat [PARAM] {FILE1 FILE2} ...\n\n' \
               'PARAMs:\n -help, -h  -- print this message\n' \
                        ' -ast, -a   -- verbose AST\n' \
                        ' -bytes, -b -- verbose bytecode\n\n' \
                'NOTE: REPL is started when there are no arguments\n')
      else:
        enableRepl = False

        with open(arg, 'r') as source:
          if justParse:
            status, ast = parse(parser, source.read(), arg)
            print(ast.pretty()) if status is not False else None

    if enableRepl:
      while True:
        source = input(Color('{autogreen}~{/green} '))

        if len(source.strip()) > 0:
          count = source.count
      
          while [count('{'), count('('), count('[')] != [count('}'), count(')'), count(']')]:
            source += '\n' +  input('... ')
            count = source.count
          
          if justParse:
            status, ast = parse(parser, source)
            print(ast.pretty()) if status is not False else None
            
  except FileNotFoundError as err:
    error(f'File \'{err.filename}\' not found')

if __name__ == '__main__':
  import sys
  main(sys.argv[1:])
