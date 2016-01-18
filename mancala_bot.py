from collections import defaultdict
from random import shuffle, choice

from slackbot.bot import respond_to
from slackbot.bot import listen_to
import re

import mancala
running_games = defaultdict(mancala.Board)
can_make_move = defaultdict(lambda: True)


def get_user(message):
    return message._client.users[message._body['user']]


def show_board(message):
    board = running_games[get_user(message)['name']]
    message.reply("```%s\n" % get_user(message)['real_name'] + board.string() + "Mancala Master```")


def check_if_game_over(message):
    username = get_user(message)['name']
    board = running_games[username]

    if board.no_more_moves():
        message.reply("Game is over")
        if board.opponent_points > board.player_points:
            message.reply(choice(
                    [
                        '%s, how does this happen :(' % username,
                        '%s, I don\'t like you anymore' % username,
                        '%s, go away and take this mancala with you, I won\'t play it anymore' % username,
                        ]))
        elif board.opponent_points < board.player_points:
            message.reply(choice(
                    [
                        '%s, ha ha ha ha looooooooser' % username,
                        '%s, I told you I always win' % username,
                        '%s, start doing something else as playing mancala is not your best ' % username,
                        '%s, flawless victory' % username,
                        '%s, that was fatality!' % username,
                        '%s, it was never more easy to win' % username,
                        ]))
        else:
            message.reply(choice(
                    [
                        '%s, to draw with you is like to loose with you :(' % username,
                        '%s, worst result ever' % username,
                        '%s, well at least I didn\'t loose' % username,
                        ]))


        del running_games[username]
        can_make_move[username] = True
        return True



@respond_to('new game', re.IGNORECASE)
def hi(message):
    username = get_user(message)['name']
    running_games[username] = mancala.Board()
    can_make_move[username] = True
    message.reply('OK, let we start a new game, I am waiting for your move %s' % username)
    show_board(message)

@respond_to('show board', re.IGNORECASE)
def hi(message):
    username = get_user(message)['name']
    running_games[username] = mancala.Board()
    message.reply('%s this is our game, is your memory *that* short?' % username)
    show_board(message)

@respond_to('(?:play )?(\d+)$', re.IGNORECASE)
def hi(message, move):
    move = int(move)
    username = get_user(message)['name']


    if not (0 < move <= 6):
        message.reply('%s, you can only play move from 1 to 6, counting from your left to right' % username)


    if can_make_move[username]:
        try:
            current_board = running_games[username].get_opponent_board()
            can_make_move[username] = current_board.make_player_move(move - 1)
            running_games[username] = current_board.get_opponent_board()
        except:
            message.reply('%s, this move was wrong!' % username)
            return

        if check_if_game_over(message):
            return

        if can_make_move[username]:

            message.reply(choice(
                    [
                        '%s, ok what next?' % username,
                        '%s, well are you going to play something?' % username,
                        '%s, please make up your mind' % username,
                        '%s, make next move' % username,
                        '%s, what are you waiting for? X-mass?' % username,

                    ])
            )
        else:
            show_board(message)
            message.reply(choice(
            [
                '%s, hmmm... I need to think' % username,
                '%s is that the best you can? Let me think' % username,
                '%s just a second, I am seeing a perfect move' % username,
                '%s total annihilation is really close, just wait' % username,
                '%s there are so many good moves to play next that I need to think for a moment' % username,
            ]))

            next_move = running_games[username].find_best_move(5)[0][0]
            message.reply("My moves are: %s" % ", ".join([str(x) for x in next_move]))

            for move in next_move:
                running_games[username].make_player_move(move - 1)

            show_board(message)
            can_make_move[username] = True
            if check_if_game_over(message):
                return

    else:
        message.reply('%s wait for your turn!' % username)
