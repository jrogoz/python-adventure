"""Offer Adventure at a custom command prompt.

Copyright 2010-2015 Brandon Rhodes.  Licensed as free software under the
Apache License, Version 2.0 as detailed in the accompanying README.txt.

"""

""" Copyright 2020-2021 Joanna Rogóż
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE‐2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied.
See the License for the specific language governing permissions and
limitations under the License. """


import argparse
import os
import re
import readline
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
        words = recognition()
        words = words.lower()
        print(words)
        words = re.findall(r'\w+', words)
        if words:
            baudout(game.do_command(words))


if __name__ == '__main__':
    try:
        loop(sys.argv[1:])
    except EOFError:
        pass
