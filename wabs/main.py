import math

####################
#       LEXER      #
####################

def Lex(text) -> tuple:
    typ = ''
    col = ''
    tokens = []
    i = 0
    comment = False
    while i < len(text):
        l = text[i]
        if comment:
            if l == '\n':
                comment = False
            i += 1
            continue
        if l == '#':
            comment = True
        elif col in ('newvar', 'output', 'add', 'sub', 'set', 'show', 'if', 'then', 'end', 'for', 'while', 'input', 'rotateleft', 'shiftleft', 'stop', 'macro', 'call', 'newarray', 'get', 'index', 'size') and typ == '':
            tokens.append({'type': 'KEYWORD', 'value': col})
            col = ''
        elif col in ('LOW', 'MID', 'HIGH') and typ == '':
            tokens.append({'type': 'CONST', 'value':col})
            col = ''
        elif col in ('==', '!=', '<', '>', '<=', '>=', 'from', 'to') and typ == '' and l == ' ':
            tokens.append({'type': 'OP', 'value':col})
            col = ''
        elif col == '-b' and typ == '':
            col = ''
            typ = 'bin'
        elif l in '01' and typ == 'bin':
            col += l
            i += 1
        elif l not in '01' and typ == 'bin':
            tokens.append({'type': 'BINNARY', 'value': col[::-1]})
            typ = ''
            col = ''
        elif l in '0123456789' and typ == '' and col == '':
            col += l
            typ = 'number'
            i += 1
        elif l in '1234567890' and typ == 'number':
            col += l
            i += 1
        elif typ == 'number' and l not in '1234567890' and col != '':
            tokens.append({'type': 'INT', 'value': int(col)})
            typ = ''
            col = ''
        elif col != '' and l in ' \n\r\t':
            tokens.append({'type': 'UNKNOWN', 'value': col})
            col = ''
            i += 1
        elif l == '\n':
            if col != '':
                tokens.append({'type': 'UNKNOWN', 'value': col})
                col = ''
            i += 1
        elif l not in ' \n\r\t':
            col += l
            i += 1
        else:
            i += 1
    if col != '':
        print('Hey something didn\'t work while lexing must be you not me')
        return (tokens, True)
    return (tokens, False)

####################
#      PARSER      #
####################

def CompressTogether(tokens) -> tuple:
    typ = ''
    col = []
    coll = []
    comp = []
    ind = -1
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t['type'] == 'KEYWORD':
            if t['value'] == 'newvar':
                typ = 'newvar'
            elif t['value'] == 'newarray':
                typ = 'newarray'
            elif t['value'] == 'size' and typ == 'newarray':
                typ = 'na_size'
            elif t['value'] == 'set' and typ == 'index':
                typ = 'index_set'
            elif t['value'] == 'set':
                typ = 'set'
            elif t['value'] == 'add':
                typ = 'add'
            elif t['value'] == 'get':
                typ = 'get'
            elif t['value'] == 'sub':
                typ = 'sub'
            elif t['value'] == 'output':
                typ = 'output'
            elif t['value'] == 'show':
                typ = 'show'
            elif t['value'] == 'if':
                typ = 'if'
            elif t['value'] == 'for':
                typ = 'for'
            elif t['value'] == 'while':
                typ = 'while'
            elif t['value'] == 'macro':
                typ = 'macro'
            elif t['value'] == 'call':
                typ = 'call'
            elif t['value'] == 'input':
                typ = 'input'
            elif t['value'] == 'index' and typ == 'get':
                typ = 'get_index'
            elif t['value'] == 'index':
                typ = 'index'
            elif t['value'] == 'call':
                typ = 'call'
            elif t['value'] == 'shiftleft':
                typ = 'shiftleft'
            elif t['value'] == 'stop' and typ == 'shiftleft':
                comp.append({'type':'shift', 'value':[col]})
                typ = ''
                col = []
            elif t['value'] == 'rotateleft':
                typ = 'rol'
            elif t['value'] == 'then' and typ == 'if':
                precoll = col
                precoll.insert(0, len(comp)-1)
                precoll.insert(1, 'if')
                coll.append(precoll)
                ind += 1
                col = []
                typ = ''
            elif t['value'] == 'then' and typ == 'macro':
                precoll = col
                precoll.insert(0, len(comp)-1)
                precoll.insert(1, 'macro')
                coll.append(precoll)
                ind += 1
                col = []
                typ = ''
            elif t['value'] == 'then' and typ == 'for':
                precoll = col
                precoll.insert(0, len(comp)-1)
                precoll.insert(1, 'for')
                coll.append(precoll)
                ind += 1
                col = []
                typ = ''
            elif t['value'] == 'then' and typ == 'while':
                precoll = col
                precoll.insert(0, len(comp)-1)
                precoll.insert(1, 'while')
                coll.append(precoll)
                ind += 1
                col = []
                typ = ''
            elif t['value'] == 'end':

                if len(coll[ind]) == 0:
                    raise(SyntaxError('There is an end endding nothing somewhere'))
                if len(coll[ind]) != 5 and coll[ind][1] == ('if' or 'while'):
                    raise(SyntaxError(f'There is an uncomplete {coll[ind][1]} statment dummy'))
                if len(coll[ind]) != 3 and coll[ind][1] == 'macro':
                    raise(SyntaxError(f'There is an uncomplete {coll[ind][1]} statment dummy'))
                if len(coll[ind]) != 7 and coll[ind][1] == 'for': 
                    raise(SyntaxError(f'There is an uncomplete {coll[ind][1]} statment dummy'))

                compen = comp[coll[ind][0]+1:]
                comp = comp[:coll[ind][0]+1]
                colltad = coll[ind][2:]
                comp.append({'type': coll[ind][1], 'value': [colltad, compen]})
                coll.pop()
                ind -= 1

            i += 1
        elif t['type'] == 'UNKNOWN':
            if typ in ('newvar', 'input'):
                comp.append({'type': typ, 'value':[t['value']]})
                typ = ''
            elif typ == 'call':
                comp.append({'type': 'call', 'value':[t['value']]})
                typ = ''
            elif typ == 'index_set':
                comp.append({'type': 'setindex', 'value':[col[0], col[1], t['value']]})
                col = []
                typ = ''
            elif typ == 'get_index':
                comp.append({'type': 'getindex', 'value':[col[0], col[1], t['value']]})
                col = []
                typ = ''
            elif typ == 'rol':
                comp.append({'type': 'rol', 'value':[t['value']]})
                typ = ''
            elif typ in ('set', 'add', 'sub', 'na_size'):
                comp.append({'type': typ, 'value':[col[0], t['value']]})
                col = []
                typ = ''
            elif typ == 'output_LOW':
                comp.append({'type': 'outlow', 'value':[t['value']]})
                typ = ''
            elif typ == 'output_MID':
                comp.append({'type': 'outmed', 'value':[t['value']]})
                typ = ''
            elif typ == 'output_HIGH':
                comp.append({'type': 'outhigh', 'value':[t['value']]})
                typ = ''
            elif typ == 'show':
                comp.append({'type': 'show', 'value':[t['value']]})
                typ = ''
            else:
                col.append(t['value'])
            i += 1
        elif t['type'] == 'INT':
            if typ in ('set', 'add', 'sub', 'na_size'):
                comp.append({'type': typ, 'value':[col[0], t['value']]})
                col = []
                typ = ''
            elif typ == 'index_set':
                comp.append({'type': 'setindex', 'value':[col[0], col[1], t['value']]})
                col = []
                typ = ''
            elif typ == 'get_index':
                comp.append({'type': 'getindex', 'value':[col[0], col[1], t['value']]})
                col = []
                typ = ''
            elif typ == 'show':
                comp.append({'type': 'show', 'value':[t['value']]})
                typ = ''
            elif typ == 'output_LOW':
                comp.append({'type': 'outlow', 'value':[t['value']]})
                typ = ''
            elif typ == 'output_MID':
                comp.append({'type': 'outmed', 'value':[t['value']]})
                typ = ''
            elif typ == 'output_HIGH':
                comp.append({'type': 'outhigh', 'value':[t['value']]})
                typ = ''
            else:
                col.append(t['value'])
            i += 1
        elif t['type'] == 'CONST':
            if typ == 'output':
                typ = f'{typ}_{t["value"]}'
                i += 1
            else:
                raise(SyntaxError('CONST is not attached to output'))
        elif t['type'] == 'BINNARY':
            if len(t['value']) != 16:
                raise(ValueError('A BINNARY value must be of 16 bits'))

            if typ == 'output_LOW':
                number = 0
                for d in range(0, len(t['value'])):
                    number += 2**d * int(t['value'][d])
                comp.append({'type': 'outlow', 'value':[number]})
                typ = ''
            elif typ == 'output_MID':
                number = 0
                for d in range(0, len(t['value'])):
                    number += 2**d * int(t['value'][d])
                comp.append({'type': 'outmed', 'value':[number]})
                typ = ''
            elif typ == 'output_HIGH':
                number = 0
                for d in range(0, len(t['value'])):
                    number += 2**d * int(t['value'][d])
                comp.append({'type': 'outhigh', 'value':[number]})
                typ = ''
            elif typ in ('set', 'add', 'sub'):
                number = 0
                for d in range(0, len(t['value'])):
                    number += 2**d * int(t['value'][d])
                comp.append({'type': typ, 'value':[col[0], number]})
                col = []
                typ = ''
            elif typ == 'show':
                number = 0
                for d in range(0, len(t['value'])):
                    number += 2**d * int(t['value'][d])
                comp.append({'type': 'show', 'value':[number]})
                typ = ''
            elif typ == 'index_set':
                number = 0
                for d in range(0, len(t['value'])):
                    number += 2**d * int(t['value'][d])
                comp.append({'type': 'setindex', 'value':[col[0], col[1], number]})
                col = []
                typ = ''
            elif typ == 'get_index':
                number = 0
                for d in range(0, len(t['value'])):
                    number += 2**d * int(t['value'][d])
                comp.append({'type': 'getindex', 'value':[col[0], col[1], number]})
                col = []
                typ = ''
            else:
                number = 0
                for d in range(0, len(t['value'])):
                    number += 2**d * int(t['value'][d])
                col.append(number)
            i += 1
        elif t['type'] == 'OP':
            col.append(t['value'])
            i += 1
        else:
            i += 1
    if col != []:
        print('The parsing proccess went wrong must be you not me')
        print(col)
        print(comp)
        return (comp, True)
    return (comp, False)

####################
#     COMPILER     #
####################

def Compile(comp, _vars, _pointer, _line, _prog, _macros) -> tuple:
    compiled = ''
    vars = _vars.copy()
    macros = _macros.copy()
    pointer = int(_pointer)
    line = int(_line)
    prog = int(_prog)
    for c in comp:

        if c['type'] == 'newvar':

            vars.update({c['value'][0]:pointer})
            pointer += 1

        elif c['type'] == 'set':

            if isinstance(c["value"][0], int):
                print(f'You can\'t put an int first in a set it has to be a variable \nline: {line}')
                break

            if isinstance(c["value"][1], int):
                compiled += f'lda {c["value"][1]}; \nsta {vars[c["value"][0]]}; \n'

            else:
                compiled += f'rda {vars[c["value"][1]]}; \nsta {vars[c["value"][0]]}; \n'

            prog += 2

        elif c['type'] == 'add':

            if isinstance(c["value"][0], int):
                print(f'You can\'t put an int first in an add it has to be a variable \nline: {line}')
                break

            if isinstance(c["value"][1], int):
                compiled += f'rda {vars[c["value"][0]]}; \nldb {c["value"][1]}; \nadd; \nsta {vars[c["value"][0]]}; \n'

            else:
                compiled += f'rda {vars[c["value"][0]]}; \nldb {vars[c["value"][1]]}; \nadd; \nsta {vars[c["value"][0]]}; \n'

            prog += 4

        elif c['type'] == 'sub':

            if isinstance(c["value"][0], int):
                print(f'You can\'t put an int first in a sub it has to be a variable \nline: {line}')
                break

            if isinstance(c["value"][1], int):
                compiled += f'rda {vars[c["value"][0]]}; \nldb {c["value"][1]}; \nsub; \nsta {vars[c["value"][0]]}; \n'

            else:
                compiled += f'rda {vars[c["value"][0]]}; \nldb {vars[c["value"][1]]}; \nsub; \nsta {vars[c["value"][0]]}; \n'
        
            prog += 4

        elif c['type'] == 'outlow':

            if isinstance(c["value"][0], int):
                compiled += f'lda {c["value"][0]}; \noutbo; \n'
            else:
                compiled += f'rda {vars[c["value"][0]]}; \noutbo; \n'
            prog += 2;
        
        elif c['type'] == 'outmed':

            if isinstance(c["value"][0], int):
                compiled += f'lda {c["value"][0]}; \noutmi; \n'
            else:
                compiled += f'rda {vars[c["value"][0]]}; \noutmi; \n'
            prog += 2;
        
        elif c['type'] == 'outhigh':

            if isinstance(c["value"][0], int):
                compiled += f'lda {c["value"][0]}; \noutto; \n'
            else:
                compiled += f'rda {vars[c["value"][0]]}; \noutto; \n'
            prog += 2;
        
        elif c['type'] == 'show':

            if isinstance(c["value"][0], int):
                compiled += f'lda {c["value"][0]}; \nshow; \n'
            else:
                compiled += f'rda {vars[c["value"][0]]}; \nshow; \n'

            prog += 2;
        
        elif c['type'] == 'if':
            if c['value'][0][1] == '==':
                part = Compile(c['value'][1], vars, pointer, line, int(prog)+5, macros)
                
                if isinstance(c["value"][0][0], int) and isinstance(c["value"][0][2], int):

                    compiled += f'lda {c["value"][0][0]}; \nldb {c["value"][0][2]}; \nsub; \njz {prog+5}; \njmp {part[4]}; \n' + part[0]
                
                elif isinstance(c["value"][0][0], int):
                    
                    compiled += f'lda {c["value"][0][0]}; \nrdb {vars[c["value"][0][2]]}; \nsub; \njz {prog+5}; \njmp {part[4]}; \n' + part[0]
                
                elif isinstance(c["value"][0][2], int):
                    
                    compiled += f'rda {vars[c["value"][0][0]]}; \nldb {c["value"][0][2]}; \nsub; \njz {prog+5}; \njmp {part[4]}; \n' + part[0]
                
                else:
                    
                    compiled += f'rda {vars[c["value"][0][0]]}; \nrdb {vars[c["value"][0][2]]}; \nsub; \njz {prog+5}; \njmp {part[4]}; \n' + part[0]

                prog = part[4]
            
            elif c['value'][0][1] == '!=':
                part = Compile(c['value'][1], vars, pointer, line, int(prog)+5, macros)
                
                if isinstance(c["value"][0][0], int) and isinstance(c["value"][0][2], int):
                    
                    compiled += f'lda {c["value"][0][0]}; \nldb {c["value"][0][2]}; \nsub; \njz {part[4]}; \njmp {prog+5}; \n' + part[0]
                
                elif isinstance(c["value"][0][0], int):
                    
                    compiled += f'lda {c["value"][0][0]}; \nrdb {vars[c["value"][0][2]]}; \nsub; \njz {part[4]}; \njmp {prog+5}; \n' + part[0]
                
                elif isinstance(c["value"][0][2], int):
                    
                    compiled += f'rda {vars[c["value"][0][0]]}; \nldb {c["value"][0][2]}; \nsub; \njz {part[4]}; \njmp {prog+5}; \n' + part[0]
                
                else:
                    
                    compiled += f'rda {vars[c["value"][0][0]]}; \nrdb {vars[c["value"][0][2]]}; \nsub; \njz {part[4]}; \njmp {prog+5}; \n' + part[0]

                prog = part[4]
            
            elif c['value'][0][1] == '<':
                part = Compile(c['value'][1], vars, pointer, line, int(prog)+5, macros)
                
                if isinstance(c["value"][0][0], int) and isinstance(c["value"][0][2], int):
                    
                    compiled += f'ldb {c["value"][0][0]}; \nlda {c["value"][0][2]-1}; \nsub; \njc {prog+5}; \njmp {part[4]}; \n' + part[0]

                elif isinstance(c["value"][0][0], int):
                    
                    compiled += f'ldb {c["value"][0][0]}; \nrda {vars[c["value"][0][2]]-1}; \nsub; \njc {prog+5}; \njmp {part[4]}; \n' + part[0]
                
                elif isinstance(c["value"][0][2], int):
                    
                    compiled += f'rdb {vars[c["value"][0][0]]}; \nlda {c["value"][0][2]-1}; \nsub; \njc {prog+5}; \njmp {part[4]}; \n' + part[0]
                
                else:
                    
                    compiled += f'rdb {vars[c["value"][0][0]]}; \nrda {vars[c["value"][0][2]]-1}; \nsub; \njc {prog+5}; \njmp {part[4]}; \n' + part[0]

                prog = part[4]
            
            elif c['value'][0][1] == '>':
                part = Compile(c['value'][1], vars, pointer, line, int(prog)+5, macros)
                
                if isinstance(c["value"][0][0], int) and isinstance(c["value"][0][2], int):
                    
                    compiled += f'lda {c["value"][0][0]}; \nldb {c["value"][0][2]}; \nsub; \njc {prog+5}; \njmp {part[4]}; \n' + part[0]

                elif isinstance(c["value"][0][0], int):
                    
                    compiled += f'lda {c["value"][0][0]}; \nrdb {vars[c["value"][0][2]]}; \nsub; \njc {prog+5}; \njmp {part[4]}; \n' + part[0]
                
                elif isinstance(c["value"][0][2], int):
                    
                    compiled += f'rda {vars[c["value"][0][0]]}; \nldb {c["value"][0][2]}; \nsub; \njc {prog+5}; \njmp {part[4]}; \n' + part[0]
                
                else:
                    
                    compiled += f'rda {vars[c["value"][0][0]]}; \nrdb {vars[c["value"][0][2]]}; \nsub; \njc {prog+5}; \njmp {part[4]}; \n' + part[0]

                prog = part[4]
            
            elif c['value'][0][1] == '<=':
                part = Compile(c['value'][1], vars, pointer, line, int(prog)+6, macros)
                
                if isinstance(c["value"][0][0], int) and isinstance(c["value"][0][2], int):
                    
                    compiled += f'ldb {c["value"][0][0]}; \nlda {c["value"][0][2]}; \nsub; \njc {prog+6}; \njz {prog+6}; \njmp {part[4]}; \n' + part[0]

                elif isinstance(c["value"][0][0], int):
                    
                    compiled += f'ldb {c["value"][0][0]}; \nrda {vars[c["value"][0][2]]}; \nsub; \njc {prog+6}; \njz {prog+6}; \njmp {part[4]}; \n' + part[0]
                
                elif isinstance(c["value"][0][2], int):
                    
                    compiled += f'rdb {vars[c["value"][0][0]]}; \nlda {c["value"][0][2]}; \nsub; \njc {prog+6}; \njz {prog+6}; \njmp {part[4]}; \n' + part[0]
                
                else:
                    
                    compiled += f'rdb {vars[c["value"][0][0]]}; \nrda {vars[c["value"][0][2]]}; \nsub; \njc {prog+6}; \njz {prog+6}; \njmp {part[4]}; \n' + part[0]

                prog = part[4]
            
            elif c['value'][0][1] == '>=':
                part = Compile(c['value'][1], vars, pointer, line, int(prog)+6, macros)
                
                if isinstance(c["value"][0][0], int) and isinstance(c["value"][0][2], int):
                    
                    compiled += f'lda {c["value"][0][0]}; \nldb {c["value"][0][2]}; \nsub; \njc {prog+6}; \njz {prog+6}; \njmp {part[4]}; \n' + part[0]

                elif isinstance(c["value"][0][0], int):
                    
                    compiled += f'lda {c["value"][0][0]}; \nrdb {vars[c["value"][0][2]]}; \nsub; \njc {prog+6}; \njz {prog+6}; \njmp {part[4]}; \n' + part[0]
                
                elif isinstance(c["value"][0][2], int):
                    
                    compiled += f'rda {vars[c["value"][0][0]]}; \nldb {c["value"][0][2]}; \nsub; \njc {prog+6}; \njz {prog+6}; \njmp {part[4]}; \n' + part[0]
                
                else:
                    
                    compiled += f'rda {vars[c["value"][0][0]]}; \nrdb {vars[c["value"][0][2]]}; \nsub; \njc {prog+6}; \njz {prog+6}; \njmp {part[4]}; \n' + part[0]

                prog = part[4]
            
            else:

                print(f'{c["value"][0][1]} Is not a valid OPERATOR for an if statment')
        
        elif c['type'] == 'for':
            if c['value'][0][1] == 'from' and c['value'][0][3] == 'to':
                vars.update({c['value'][0][0]: pointer})
                pointer += 1
                if isinstance(c['value'][0][2], int):
                    compiled += f'lda {c["value"][0][2]}; \nsta {vars[c["value"][0][0]]}; \n'
                else:
                    compiled += f'rda {vars[c["value"][0][2]]}; \nsta {vars[c["value"][0][0]]}; \n'
                prog += 2
                part = Compile(c['value'][1], vars, pointer, line, int(prog)+5, macros)

                if isinstance(c["value"][0][4], int):
                    compiled += f'rdb {vars[c["value"][0][0]]}; \nlda {c["value"][0][4]-1}; \nsub; \njc {prog+5}; \njmp {part[4]+5}; \n' + part[0] + f'rda {vars[c["value"][0][0]]}; \nldb 1; \nadd; \nsta {vars[c["value"][0][0]]}; \njmp {prog}; \n'
                else:
                    compiled += f'rdb {vars[c["value"][0][0]]}; \nlda {vars[c["value"][0][4]]-1}; \nsub; \njc {prog+5}; \njmp {part[4]+5}; \n' + part[0] + f'rda {vars[c["value"][0][0]]}; \nldb 1; \nadd; \nsta {vars[c["value"][0][0]]}; \njmp {prog}; \n'

                prog = part[4] + 5

                vars.pop(c['value'][0][0])
                pointer -= 1
            
            else:

                print('for statemnt is not correct')
                
        elif c['type'] == 'while':
            if c['value'][0][1] == '==':
                part = Compile(c['value'][1], vars, pointer, line, int(prog)+5, macros)
                
                if isinstance(c["value"][0][0], int) and isinstance(c["value"][0][2], int):

                    compiled += f'lda {c["value"][0][0]}; \nldb {c["value"][0][2]}; \nsub; \njz {prog+5}; \njmp {part[4]+1}; \n' + part[0] + f'jmp {prog}; \n'
                
                elif isinstance(c["value"][0][0], int):
                    
                    compiled += f'lda {c["value"][0][0]}; \nrdb {vars[c["value"][0][2]]}; \nsub; \njz {prog+5}; \njmp {part[4]+1}; \n' + part[0] + f'jmp {prog}; \n'
                
                elif isinstance(c["value"][0][2], int):
                    
                    compiled += f'rda {vars[c["value"][0][0]]}; \nldb {c["value"][0][2]}; \nsub; \njz {prog+5}; \njmp {part[4]+1}; \n' + part[0] + f'jmp {prog}; \n'
                
                else:
                    
                    compiled += f'rda {vars[c["value"][0][0]]}; \nrdb {vars[c["value"][0][2]]}; \nsub; \njz {prog+5}; \njmp {part[4]+1}; \n' + part[0] + f'jmp {prog}; \n'

                prog = part[4]
            
            elif c['value'][0][1] == '!=':
                part = Compile(c['value'][1], vars, pointer, line, int(prog)+5, macros)
                
                if isinstance(c["value"][0][0], int) and isinstance(c["value"][0][2], int):
                    
                    compiled += f'lda {c["value"][0][0]}; \nldb {c["value"][0][2]}; \nsub; \njz {part[4]+1}; \njmp {prog+5}; \n' + part[0] + f'jmp {prog}; \n'
                
                elif isinstance(c["value"][0][0], int):
                    
                    compiled += f'lda {c["value"][0][0]}; \nrdb {vars[c["value"][0][2]]}; \nsub; \njz {part[4]+1}; \njmp {prog+5}; \n' + part[0] + f'jmp {prog}; \n'
                
                elif isinstance(c["value"][0][2], int):
                    
                    compiled += f'rda {vars[c["value"][0][0]]}; \nldb {c["value"][0][2]}; \nsub; \njz {part[4]+1}; \njmp {prog+5}; \n' + part[0] + f'jmp {prog}; \n'
                
                else:
                    
                    compiled += f'rda {vars[c["value"][0][0]]}; \nrdb {vars[c["value"][0][2]]}; \nsub; \njz {part[4]+1}; \njmp {prog+5}; \n' + part[0] + f'jmp {prog}; \n'

                prog = part[4]
            
            elif c['value'][0][1] == '<':
                part = Compile(c['value'][1], vars, pointer, line, int(prog)+5, macros)
                
                if isinstance(c["value"][0][0], int) and isinstance(c["value"][0][2], int):
                    
                    compiled += f'ldb {c["value"][0][0]}; \nlda {c["value"][0][2]-1}; \nsub; \njc {prog+5}; \njmp {part[4]+1}; \n' + part[0] + f'jmp {prog}; \n'

                elif isinstance(c["value"][0][0], int):
                    
                    compiled += f'ldb {c["value"][0][0]}; \nrda {vars[c["value"][0][2]]-1}; \nsub; \njc {prog+5}; \njmp {part[4]+1}; \n' + part[0] + f'jmp {prog}; \n'
                
                elif isinstance(c["value"][0][2], int):
                    
                    compiled += f'rdb {vars[c["value"][0][0]]}; \nlda {c["value"][0][2]-1}; \nsub; \njc {prog+5}; \njmp {part[4]+1}; \n' + part[0] + f'jmp {prog}; \n'
                
                else:
                    
                    compiled += f'rdb {vars[c["value"][0][0]]}; \nrda {vars[c["value"][0][2]]-1}; \nsub; \njc {prog+5}; \njmp {part[4]+1}; \n' + part[0] + f'jmp {prog}; \n'

                prog = part[4]
            
            elif c['value'][0][1] == '>':
                part = Compile(c['value'][1], vars, pointer, line, int(prog)+5, macros)
                
                if isinstance(c["value"][0][0], int) and isinstance(c["value"][0][2], int):
                    
                    compiled += f'lda {c["value"][0][0]}; \nldb {c["value"][0][2]}; \nsub; \njc {prog+5}; \njmp {part[4]+1}; \n' + part[0] + f'jmp {prog}; \n'

                elif isinstance(c["value"][0][0], int):
                    
                    compiled += f'lda {c["value"][0][0]}; \nrdb {vars[c["value"][0][2]]}; \nsub; \njc {prog+5}; \njmp {part[4]+1}; \n' + part[0] + f'jmp {prog}; \n'
                
                elif isinstance(c["value"][0][2], int):
                    
                    compiled += f'rda {vars[c["value"][0][0]]}; \nldb {c["value"][0][2]}; \nsub; \njc {prog+5}; \njmp {part[4]+1}; \n' + part[0] + f'jmp {prog}; \n'
                
                else:
                    
                    compiled += f'rda {vars[c["value"][0][0]]}; \nrdb {vars[c["value"][0][2]]}; \nsub; \njc {prog+5}; \njmp {part[4]+1}; \n' + part[0] + f'jmp {prog}; \n'

                prog = part[4]
            
            elif c['value'][0][1] == '<=':
                part = Compile(c['value'][1], vars, pointer, line, int(prog)+6, macros)
                
                if isinstance(c["value"][0][0], int) and isinstance(c["value"][0][2], int):
                    
                    compiled += f'ldb {c["value"][0][0]}; \nlda {c["value"][0][2]}; \nsub; \njc {prog+6}; \njz {prog+6}; \njmp {part[4]+1}; \n' + part[0] + f'jmp {prog}; \n'

                elif isinstance(c["value"][0][0], int):
                    
                    compiled += f'ldb {c["value"][0][0]}; \nrda {vars[c["value"][0][2]]}; \nsub; \njc {prog+6}; \njz {prog+6}; \njmp {part[4]+1}; \n' + part[0] + f'jmp {prog}; \n'
                
                elif isinstance(c["value"][0][2], int):
                    
                    compiled += f'rdb {vars[c["value"][0][0]]}; \nlda {c["value"][0][2]}; \nsub; \njc {prog+6}; \njz {prog+6}; \njmp {part[4]+1}; \n' + part[0] + f'jmp {prog}; \n'
                
                else:
                    
                    compiled += f'rdb {vars[c["value"][0][0]]}; \nrda {vars[c["value"][0][2]]}; \nsub; \njc {prog+6}; \njz {prog+6}; \njmp {part[4]+1}; \n' + part[0] + f'jmp {prog}; \n'

                prog = part[4]
            
            elif c['value'][0][1] == '>=':
                part = Compile(c['value'][1], vars, pointer, line, int(prog)+6, macros)
                
                if isinstance(c["value"][0][0], int) and isinstance(c["value"][0][2], int):
                    
                    compiled += f'lda {c["value"][0][0]}; \nldb {c["value"][0][2]}; \nsub; \njc {prog+6}; \njz {prog+6}; \njmp {part[4]+1}; \n' + part[0] + f'jmp {prog}; \n'

                elif isinstance(c["value"][0][0], int):
                    
                    compiled += f'lda {c["value"][0][0]}; \nrdb {vars[c["value"][0][2]]}; \nsub; \njc {prog+6}; \njz {prog+6}; \njmp {part[4]+1}; \n' + part[0] + f'jmp {prog}; \n'
                
                elif isinstance(c["value"][0][2], int):
                    
                    compiled += f'rda {vars[c["value"][0][0]]}; \nldb {c["value"][0][2]}; \nsub; \njc {prog+6}; \njz {prog+6}; \njmp {part[4]+1}; \n' + part[0] + f'jmp {prog}; \n'
                
                else:
                    
                    compiled += f'rda {vars[c["value"][0][0]]}; \nrdb {vars[c["value"][0][2]]}; \nsub; \njc {prog+6}; \njz {prog+6}; \njmp {part[4]+1}; \n' + part[0] + f'jmp {prog}; \n'

                prog = part[4]
            
            else:
                raise(SyntaxError(f'{c["value"][0][1]} is not a valid operator for a while loop'))

            prog += 1
        
        elif c['type'] == 'rol':
            compiled += f'rda {vars[c["value"][0]]}; \nrol; \nsta {vars[c["value"][0]]}; \n'
            prog += 3
        
        elif c['type'] == 'shift':
            for s in c['value'][0]:
                compiled += f'rda {vars[s]}; \nrolc; \nsta {vars[s]}; \n'
                prog += 3

        elif c['type'] == 'macro':
            parts = Compile(c['value'][1], vars, pointer, line, prog+1, macros)
            compiled += f'jmp {parts[4]+1}; \n' + parts[0] + 'ret; \n'
            macros.update({c['value'][0][0]: prog+1})
            prog = parts[4]+1

        elif c['type'] == 'call':
            compiled += f'cal {macros[c["value"][0]]}; \n'
            prog += 1

        elif c['type'] == 'na_size':
            arr = []
            v1 = 0
            if isinstance(c['value'][1], int):
                v1 = c['value'][1]
            else:
                raise(SyntaxError('Size of an array must be an integer'))

            for ai in range(0, v1):
                arr.append(pointer+ai)
            vars.update({c['value'][0]:arr})
            pointer += v1
        
        elif c['type'] == 'setindex':

            if isinstance(c['value'][1], int) and isinstance(c['value'][2], int):

                if c['value'][0] in vars:
                    if isinstance(vars[c['value'][0]], list):
                        if -1 < c["value"][1] < len(vars[c['value'][0]]):
                            compiled += f'lda {c["value"][2]}; \nsta {vars[c["value"][0]][c["value"][1]]}; \n'
                            prog += 2
                        else:
                            raise(IndexError(f"Array isn't that big/small index:{v1}"))
                    else:
                        raise(SyntaxError("Can't get index of a regular variable"))
                else:
                    raise(SyntaxError("Can access a non existant variable"))

            elif isinstance(c['value'][1], int):
                
                if c['value'][0] in vars:
                    if isinstance(vars[c['value'][0]], list):
                        if -1 < c["value"][1] < len(vars[c['value'][0]]):
                            compiled += f'rda {vars[c["value"][2]]}; \nsta {vars[c["value"][0]][c["value"][1]]}; \n'
                            prog += 2
                        else:
                            raise(IndexError(f"Array isn't that big/small index:{v1}"))
                    else:
                        raise(SyntaxError("Can't get index of a regular variable"))
                else:
                    raise(SyntaxError("Can access a non existant variable"))

            elif isinstance(c['value'][2], int):
                
                if c['value'][0] in vars:
                    if isinstance(vars[c['value'][0]], list):
                        compiled += f'rda {vars[c["value"][1]]}; \nldb {vars[c["value"][0]][0]}; \nadd; \nldatmem; \nlda {c["value"][2]}; \nstatmem; \n'
                        prog += 6
                    else:
                        raise(SyntaxError("Can't get index of a regular variable"))
                else:
                    raise(SyntaxError("Can access a non existant variable"))

            else:
                if c['value'][0] in vars:
                    if isinstance(vars[c['value'][0]], list):
                        compiled += f'rda {vars[c["value"][1]]}; \nldb {vars[c["value"][0]][0]}; \nadd; \nldatmem; \nrda {vars[c["value"][2]]}; \nstatmem; \n'
                        prog += 6
                    else:
                        raise(SyntaxError("Can't get index of a regular variable"))
                else:
                    raise(SyntaxError("Can access a non existant variable"))
        
        elif c['type'] == 'getindex':

            if isinstance(c['value'][2], int):
                if c['value'][0] in vars:
                    if isinstance(vars[c['value'][1]], list):
                        if -1 < c['value'][2] < len(vars[c['value'][1]]):
                            compiled += f'rda {vars[c["value"][1]][c["value"][2]]}; \nsta {vars[c["value"][0]]}; \n'
                            prog += 2
                        else:
                            raise(IndexError(f"Array isn't that big/small index:{c['value'][2]}"))
                    else:
                        raise(SyntaxError("Can't get index of a regular variable"))
                else:
                    raise(SyntaxError("Can access a non existant variable"))
            else:
                if c['value'][0] in vars:
                    if isinstance(vars[c['value'][1]], list):
                        compiled += f'rda {vars[c["value"][2]]}; \nldb {vars[c["value"][1]][0]}; \nadd; \nldatmem; \nrdafmem; \nsta {vars[c["value"][0]]}; \n'
                        prog += 6
                    else:
                        raise(SyntaxError("Can't get index of a regular variable"))
                else:
                    raise(SyntaxError("Can access a non existant variable"))

        elif c['type'] == 'input':
            if isinstance(c['value'][0], int):
                raise(SyntaxError("CAN'T INPUT TO A NUMBER IT HAS TO BE A VARIABLE"))
            else:
                compiled += f'rdin; \nsta {vars[c["value"][0]]}; \n'
                prog += 2

        line += 1
    if prog >= 65536:
        print("Hey dummy i have just seen that your program exceeds the computers code storage capcity so sorry it wont compile")
        return (compiled, vars, pointer, line, prog, macros, False)
    return (compiled, vars, pointer, line, prog, macros, True)

####################
#     HEXCODES     #
####################

def DecimalToHex(decimal) -> str:
    # 1, 16, 256, 4096
    sthex = '0123456789ABCDEFG'

    stdecimal = int(decimal)
    stdecimal /= 4096
    th4 = math.floor(stdecimal)

    stdecimal = int(decimal) - (th4*4096)
    stdecimal /= 256
    th3 = math.floor(stdecimal)

    stdecimal = int(decimal) - ((th4*4096)+(th3*256))
    stdecimal /= 16
    th2 = math.floor(stdecimal)

    stdecimal = int(decimal) - ((th4*4096)+(th3*256)+(th2*16))
    th1 = math.floor(stdecimal)

    return sthex[th4] + sthex[th3] + sthex[th2] + sthex[th1]
    

def Coolify(compiled) -> str:
    coolstr = ''
    i = 1
    for line in compiled.split('\n'):
        if len(line) == 0:
            continue
        lineless = line.removesuffix(' ')
        words = lineless.split(' ')
        if words[0] == 'lda':
            coolstr += '0xF083'
        elif words[0] == 'ldb':
            coolstr += '0x2C4D'
        elif words[0] == 'sta':
            coolstr += '0xB393'
        elif words[0] == 'stb':
            coolstr += '0x3C3D'
        elif words[0] == 'rda':
            coolstr += '0xEF59'
        elif words[0] == 'rdb':
            coolstr += '0xF6A3'
        elif words[0] == 'jmp':
            coolstr += '0xCA5C'
        elif words[0] == 'jc':
            coolstr += '0xCA44'
        elif words[0] == 'jz':
            coolstr += '0xCA54'
        elif words[0] == 'outbo':
            coolstr += '0xABBE'
        elif words[0] == 'outmi':
            coolstr += '0xABB6'
        elif words[0] == 'outto':
            coolstr += '0xABAE'
        elif words[0] == 'show':
            coolstr += '0xEEEE'
        elif words[0] == 'add':
            coolstr += '0xAC7B'
        elif words[0] == 'sub':
            coolstr += '0xD313'
        elif words[0] == 'cal':
            coolstr += '0x9575'
        elif words[0] == 'ret':
            coolstr += '0xEEAD'
        elif words[0] == 'rdin':
            coolstr += '0xBDEF'
        elif words[0] == 'rol':
            coolstr += '0x9D6A'
        elif words[0] == 'rolc':
            coolstr += '0x95D7'
        elif words[0] == 'ldatmem':
            coolstr += '0x8DEF'
        elif words[0] == 'statmem':
            coolstr += '0x94A5'
        elif words[0] == 'rdafmem':
            coolstr += '0xDD9B'
        else:
            raise(NameError(f"Name not't defined {words[0]}"))
        
        if len(words) == 1:
            coolstr += '0000; '
        elif words[1].isdigit():
            coolstr += DecimalToHex(int(words[1])) + '; '


        if i == 8:
            coolstr += '\n'
            i = 0
        i += 1
    return coolstr

####################
#    FILEREADING   #
####################

with open('main.wabs', 'r') as file:
    coolifyyn = ''
    while coolifyyn not in ('yes', 'no'):
        coolifyyn = input("Would you like to convert to hexadecimal (yes/no)").lower()
    filetext = file.read()
    tokens, error1 = Lex(filetext + '\n')
    if error1 is False:
        compr, error2 = CompressTogether(tokens)
        if error2 is False:
            parts = Compile(compr, {}, 1, 1, 1, {})
            if parts[6]:
                with open('output.txt', 'w') as out:
                    if coolifyyn == 'yes':
                        out.write(Coolify(parts[0].replace(';', '')))
                    else:
                        out.write(parts[0])
