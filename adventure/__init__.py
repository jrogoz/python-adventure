"""The Adventure game.

Copyright 2010-2015 Brandon Rhodes.  Licensed as free software under the
Apache License, Version 2.0 as detailed in the accompanying README.txt.

"""
import sys
from .speech import synthesis

if sys.version_info <= (3,):
    raise RuntimeError('Alas, Adventure requires Python 3 or later')

def load_advent_dat(data):
    import os
    from .data import parse

    datapath = os.path.join(os.path.dirname(__file__), 'advent.dat')
    with open(datapath, 'r', encoding='ascii') as datafile:
        parse(data, datafile)

def play(seed=None):
    """Turn the Python prompt into an Adventure game.

    With optional the `seed` argument the caller can supply an integer
    to start the Python random number generator at a known state.

    """
    global _game

    from .game import Game
    from .prompt import install_words

    _game = Game(seed)
    load_advent_dat(_game)
    install_words(_game)
    _game.start()
    print(_game.output[:-1])
    synthesis(_game.output[:-1])

def resume(savefile, quiet=False):
    global _game

    from .game import Game
    from .prompt import install_words

    _game = Game.resume(savefile)
    install_words(_game)
    if not quiet:
        print('GAME RESTORED\n')
        synthesis('game restored')

import sys
from time import sleep
from adventure import load_advent_dat
from adventure.game import Game
from adventure.speech import synthesis, recognition

BAUD = 1200

def baudout(s):
    out = sys.stdout
    for c in s:
        sleep(9. / BAUD)  # 8 bits + 1 stop bit @ the given baud rate
        out.write(c)
        out.flush()
    synthesis(s.lower())

def loop(args):
    parser = argparse.ArgumentParser(
        description='Adventure into the Colossal Caves.',
        prog='{} -m adventure'.format(os.path.basename(sys.executable)))
    parser.add_argument(
        'savefile', nargs='?', help='The filename of game you have saved.')
    args = parser.parse_args(args)

    if args.savefile is None:
        game = Game()
        load_advent_dat(game)
        game.start()
        baudout(game.output)


    else:
        game = Game.resume(args.savefile)
        baudout('GAME RESTORED\n')

    while not game.is_finished:
        # line = input('> ').lower()
        # words = re.findall(r'\w+', line)
        line = recognition()
        if line is not None:
            line = line.lower()
        print(line)
        words = re.findall(r'\w+', line)
        if words:
            baudout(game.do_command(words))


if __name__ == '__main__':
    try:
        loop(sys.argv[1:])
    except EOFError:
        pass
