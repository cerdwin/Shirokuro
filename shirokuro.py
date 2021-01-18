#!/usr/bin/python3
import sys
import pycosat
import pprint
import numpy as np
import copy

def create_double_table(table):
    '''
    This function takes in an nxn table and outputs a somewhat magnified version of said table so that each cell situated
    in the interior of the original table is "padded" with zeros. This is so that I can solve better cases when circles are
    thightly packed together and 'see' which are connected with which.
    :param table: 2d array of dimension nxn, filled with strings.
    :return: A magnified version of the table of size (2*n-1)x(2*n-1)
    '''
    length = len(table)
    padding_line = ['0' for i in range(length*2 -1) ]
    new_grid = []
    index = 0
    for row in table:
        new_row = []
        for i in range(length):
            new_row.append(row[i])
            if i != length-1:
                new_row.append('0')
        new_grid.append(new_row)
        if index != length -1:
            new_grid.append(copy.deepcopy(padding_line))
        index += 1
    return new_grid

def create_table():
    '''
    Simple function, takes in a string from stdin and creates an nxn table from it
    :return: An nxn table representing the Shirokuro grid
    '''
    for line in sys.stdin:
        input_string = line
        break
    grid = []
    counter = 0
    size = int(np.sqrt(len(input_string)))
    row = []
    for i in range(size):
        for s in  range(counter, counter +size):
            row.append(input_string[s])
        grid.append(row)
        row = []
        counter+=size
    return grid


def within_bounds(position, direction, width):
    if position[0]+direction[0] < 0 or position[0]+direction[0] >= width or position[1]+direction[1] < 0 or position[1]+direction[1] >= width:
        return False
    return True
def convert_to_cnf(clause, rest):
    # print('midresulting...')
    if len(rest) == 0:
        # print('returning:', clause)
        return clause
    new_clause = []
   #  print('clause:', clause, 'rest:', rest)
    for item in clause:
        # print('item:', item)
        temp = item[:] # [1]
        to_join = rest[0]
        # print('to join', to_join)
        for x in to_join:
            # print('adding:', x)
            temp.append(x)
            new_clause.append(temp)
           #  print('it gives', temp, 'item is:', item)
            temp = item[:]
    return convert_to_cnf(new_clause, rest[1:])

def shrink(table):
    # print("TABLE:")
    # pprint.pprint(table)
    result_string = ''
    for y in range(len(table)):
        for x in range(len(table)):
            if y % 2 == 0 and x % 2 == 0:
                # print("i want to add:", table[y][x])
                result_string = result_string + str(table[y][x])
    # print(result_string)
    return result_string


def resolve(width, my_map, altered, num2coord):
    brand_new = copy.deepcopy(altered)
    #print(my_map)
    #pprint.pprint(brand_new)
    # print('my map:', my_map)
    # print('my legend', num2coord)
    counter = 0
    for item in my_map:
        #print('item:', item)
        if item > 0:
            # print('adding star for item:', item, 'located at:', num2coord[item])
            counter+=1
            x_pos = num2coord[item][0]
            y_pos = num2coord[item][1]
            # print('before:')
            # pprint.pprint(brand_new)
            brand_new[x_pos][y_pos] = '*'
            # print('current state:')
            # pprint.pprint(brand_new)
    # print('counter:', counter)
    # pprint.pprint(brand_new)
    # print("MEZERA")
    #print('length:', len(brand_new))
    counter = 0

    #lista = [str(i) for i in range(len(brand_new))]
   # print("   ",lista)
    #for thing in brand_new:
     #   print(counter, ':', thing)
     #   counter+=1
    for i in range(len(brand_new)):
        for x in range(len(brand_new)):
            if brand_new[i][x] == 'w' or brand_new[i][x] == 'b':
                # West
                if x > 0 and (brand_new[i][x-1] == '*' or brand_new[i][x-1] == 'H'):
                    brand_new[i][x] = 'W'
                elif i >0 and (brand_new[i-1][x] == '*' or brand_new[i-1][x] == 'V'):
                    brand_new[i][x] = 'N'
                elif x < len(brand_new)-1 and (brand_new[i][x+1] == '*' or brand_new[i][x+1] == 'H'):
                    brand_new[i][x] = 'E'
                elif i < len(brand_new)-1 and (brand_new[i+1][x] == '*' or brand_new[i+1][x] == 'V'):
                    brand_new[i][x] = 'S'
                #else:
                   # print('error at position', i, x, 'where we have', brand_new[i][x])
                  #  if i > 0:
                  #      print(brand_new[i-1][x])
                 #   else:
                 #       print("NAHORU")
                 #   if x > 0:
                 #       print (brand_new[i][x-1])
                 #   else:
                 #       print('DOLEVA')
                 #   if i < len(brand_new)-1:
                 #       print(brand_new[i+1][x])
                 #   else:
                 #       print('DOLU')
                 #   if x < len(brand_new)-1:
                 #       print (brand_new[i][x+1])
                 #   else:
                 #       print ('DOPRAVA')

            elif brand_new[i][x] == '*':
                if x > 0 and (brand_new[i][x-1] == 'H' or brand_new[i][x-1] == 'E'):
                    brand_new[i][x] = 'H'
                elif i >0 and (brand_new[i-1][x] == 'V' or brand_new[i-1][x] == 'S'):
                    brand_new[i][x] = 'V'
                else:
                    brand_new[i][x] = '0'
                #else:
                    #print('EXCEPTION at:', 'i:', i, 'x:', x)
                   # if i > 0:
                     #   print(brand_new[i-1][x])
                    #else:
                     #   print("NAHORU")
                 #   if x > 0:
                      #  print (brand_new[i][x-1])
                    #else:
                       # print('DOLEVA')
                 #   if i < len(brand_new)-1:
                       # print(brand_new[i+1][x])
                    #else:
                       # print('DOLU')
                  #  if x < len(brand_new)-1:
                       # print (brand_new[i][x+1])
                    #else:
                      #  print ('DOPRAVA')
                  #  brand_new[i][x] = 'Z'
    counter = 0
   # print("   ", lista)
   # for thing in brand_new:
    #    print(counter, ':', thing)
    #    counter += 1
    return shrink(brand_new)



if __name__ == '__main__':
    inputting = 'w000b0w00w0bww0b0w000b0w00w0bww0b00b0wwb00w0000b00w0b0wwb00w0000b00w00000b0ww0000bbw000000b0ww0000bbw0b000b00b000w00000b000b00b000w00000bwb00w00000w0w0bbbwb00w00000w0w0bb0bb00w00000000w0b0bb00w00000000w0bw0w0w00wbb000bbw0w0w0w00wbb000bbw0wb0000bw00bb00w0wwb0000bw00bb00w0w0bb0b0w00b0w0wbw00bb0b0w00b0w0wbw00w0b0wbw0b0b0000w0w0b0wbw0b0b0000w00bwb0w00www000w000bwb0w00www000w000wbb0bwbbw00000000wbb0bwbbw00000000000wb0b00b0bwb000000wb0b00b0bwb0000www0b0w000w0b0000www0b0w000w0b0w0b00b0000b0bwbw0w0b00b0000b0bwbw0wbwbw0bwwb000w0b0wbwbw0bwwb000w0b0000bwbw000wb0wb0b000bwbw000wb0wb0bw000b0w00w0bww0b0w000b0w00w0bww0b00b0wwb00w0000b00w0b0wwb00w0000b00w00000b0ww0000bbw000000b0ww0000bbw0b000b00b000w00000b000b00b000w00000bwb00w00000w0w0bbbwb00w00000w0w0bb0bb00w00000000w0b0bb00w00000000w0bw0w0w00wbb000bbw0w0w0w00wbb000bbw0wb0000bw00bb00w0wwb0000bw00bb00w0w0bb0b0w00b0w0wbw00bb0b0w00b0w0wbw00w0b0wbw0b0b0000w0w0b0wbw0b0b0000w00bwb0w00www000w000bwb0w00www000w000wbb0bwbbw00000000wbb0bwbbw00000000000wb0b00b0bwb000000wb0b00b0bwb0000www0b0w000w0b0000www0b0w000w0b0w0b00b0000b0bwbw0w0b00b0000b0bwbw0wbwbw0bwwb000w0b0wbwbw0bwwb000w0b0000bwbw000wb0wb0b000bwbw000wb0wb0b'
    grid = copy.deepcopy(create_table())
    #
    # pprint.pprint(grid)
    width = height = len(grid)
    altered = copy.deepcopy(create_double_table(grid)) # a double the size table, I make this so I can tell
    circles = []
    whites = []
    blacks = []
    coord2num = {}
    index = 0
    for i in range(width * 2 - 1):
        for x in range(height * 2 - 1):
            current = altered[i][x]
            coord2num[(i, x)] = index
            if current == 'b' or current == 'w':
                if current == 'b':
                    blacks.append((i, x))
                else:
                    whites.append((i, x))
            index += 1
    num2coord = {v: k for k, v in coord2num.items()}
    if True:
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        final_clauses = []
        for white_circle in whites:
            clauses = []
            for direction in directions:
                new_clause = []
                position = white_circle
                while within_bounds(position, direction, width*2-1):
                    position = (position[0]+direction[0], position[1]+direction[1])
                    if altered[position[0]][position[1]] == '0':
                        new_clause.append(coord2num[position])
                        # pridej taky z kazde strany 'padding' tak, ze nesmi kolem byt nic nez nula
                        if len(altered) > position[0]+direction[1] >= 0 and len(altered) > position[1] + direction[
                            0] >= 0:
                            temp_pos = (position[0]+direction[1], position[1]+direction[0])
                            new_clause.append(-coord2num[temp_pos])
                        if len(altered) > position[1]-direction[0] >= 0 and len(altered) > position[0] - direction[
                            1] >= 0:
                            temp_pos = (position[0] - direction[1], position[1] - direction[0])
                            new_clause.append(-coord2num[temp_pos])

                    elif altered[position[0]][position[1]] == 'b':
                        #########################
                        for dir in directions: # surrounding position around the black part
                            if within_bounds(position, dir, width*2-1):
                                new_pos = (position[0] + dir[0], position[1] + dir[1])
                                if coord2num[new_pos] not in new_clause and altered[new_pos[0]][new_pos[1]] == '0':
                                    idx = coord2num[new_pos]
                                    new_clause.append(-idx)
                        position = white_circle
                        for dir in directions: # surrounding position around the white part
                            if within_bounds(position, dir, width*2-1):
                                new_pos = (position[0] + dir[0], position[1] + dir[1])
                                if  coord2num[new_pos] not in new_clause and altered[new_pos[0]][new_pos[1]] == '0':
                                    idx = coord2num[new_pos]
                                    new_clause.append(-idx)
                        #######################
                        clauses.append(new_clause)
                        break
                    else:
                        break
            final_clauses.append(clauses)
        reworked_grid = []
        for i in range(len(altered)):
            temp = []
            for x in range(len(altered)):
                temp.append(coord2num[(i, x)])
            reworked_grid.append(temp)
        # pprint.pprint(reworked_grid)
        # print(final_clauses)
        terms = []
        for clause in final_clauses:
            if len(clause) > 0:
                first_clause = clause[0]
                for i in range(len(first_clause)):
                    first_clause[i] = [first_clause[i]]
                rest = clause[1:]
                midresult = convert_to_cnf(first_clause, rest)
                # print('////////////////midresult:', midresult)
                terms.append(midresult[:])
        # print(terms)
        s = []
        for item in terms:
            for clause in item:
                s.append(clause)
        my_map = pycosat.solve(s)
        if my_map[0] == 'U':
            print('X')
        else:
            print(resolve(width, my_map, altered, num2coord))





