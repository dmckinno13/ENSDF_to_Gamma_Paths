######
#
# Author: D. V. McKinnon
# Date:   2019-05-15
# Purpose:
#          File to read in ENSDF file for beta-decay and break it into a
#          file for each gamma path.
#
######


def readin(filename):
    '''reads a file, closes it, and returns lines'''
    inf = open(filename, 'r')
    lines = inf.readlines()
    inf.close()
    return lines


def level_grab(lines, daughter):
    '''grabs the levels out of an ENSDF file'''
    levels = []
    for line in lines[::-1]:
        lin = line.split()
        if len(lin) != 0:
            if len(lin[0]) == len(daughter):
                if lin[1] == 'L':
                    levels.append(lin[2])
    return levels


def gamma_builder(lines, daughter):
    '''grabs gammas out of an ENSDF file and associates them with a level'''
    gamma_dict = {}
    level = ''
    for line in lines:
        lin = line.split()
        if len(lin) != 0:
            if len(lin[0]) == len(daughter):
                for i in range(len(lin)):  # just use lin[2] since it is static
                    if lin[i] == 'L':
                        level = lin[i+1]
                    if lin[i] == 'G':
                        gamma_dict[lin[i+1]] = level
    return gamma_dict


def find_next_level(level, gamma, levels, eps=1.):
    '''finds new level after subtracting gamma from current level'''
    next_level = float(level) - float(gamma)
    for nlvl in levels:
        if float(nlvl) > next_level - eps and float(nlvl) < next_level + eps:
            return nlvl
    return 'no level'


def path_finder(levels, gammas, eps=1.):
    '''finds and returns the paths from each level'''
    paths = []
    for lvl in levels:
        for gamma in gammas:
            if gammas[gamma] == lvl:
                nlvl = find_next_level(lvl, gamma, levels, eps)
                print('Level: ' + lvl)
                print('  Gamma: ' + gamma + ' , Next Level: ' + nlvl)
                path = ['L' + lvl, 'G' + gamma, 'L' + nlvl]
                while nlvl != '0.0':
                    for gam in gammas:
                        if gammas[gam] == nlvl:
                            nlvl = find_next_level(nlvl, gam, levels)
                            print('  Gamma: ' + gam + ' , Next Level: ' + nlvl)
                            path.append('G' + gam)
                            path.append('L' + nlvl)
                paths.append(path)
    return paths


def set_up(filename, daughter):
    '''
    performs a quick set up, returning lines, levels, and gammas to be
    used with other functions
    INPUT: path to file (string) and daughter (string) ex: 97Rb
    '''
    lines = readin(filename)
    levels = level_grab(lines, daughter)
    gammas = gamma_builder(lines, daughter)
    return lines, levels, gammas


def value_to_decimal(string):
    s = ''
    c = 1
    char = string[c]
    while char != '.':
        s += char
        c += 1
        if c == len(string):
            return s
        char = string[c]
    return s


def write_paths(paths, lines, nuclei):
    count = 0
    for path in paths:
        level = value_to_decimal(path[0])
        filename = nuclei + '_' + level + 'L'
        for item in path:
            if item[0] == 'G':
                gamma = value_to_decimal(item)
                filename += '_'+gamma+'g'
        filename += '.ens'
        ouf = open(filename, 'w')
        for line in lines[:-1]:
            if line[7] + line[9:18].strip() in path:
                ouf.write(line)
            else:
                ouf.write(line[:6]+'c'+line[7:])
        ouf.close()
        count += 1
    return 0


def run(filename, nuclei, daughter, eps=1.0):
    '''Run code to find lines, levels, gammas, and paths, and write to file.'''
    lines, levels, gammas = set_up(filename, daughter)
    paths = path_finder(levels, gammas, eps)
    x = write_paths(paths, lines, nuclei)
    return lines, levels, gammas, paths
