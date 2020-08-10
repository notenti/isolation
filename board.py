from time import time
from enum import Enum
import copy
from typing import List, Set, Tuple, Union, Optional, Any
from dataclasses import dataclass
from player import Player


class State(Enum):
    """Representation of space state."""
    BLANK = ' '
    BLOCKED = 'X'
    TRAIL = 'O'


Space = Tuple[int, int]


@dataclass
class Queen:
    """Represents Queen."""
    token: str
    last_move: Space = (-1, -1)


Gameboard = List[List[Union[State, str]]]


class Board:
    def __init__(self, p1: Player, p2: Player, width: int = 7, height: int = 7) -> None:
        self.width = width
        self.height = height

        self.__p1__ = p1
        self.__p2__ = p2

        self.__q1__ = Queen('Q1')
        self.__q2__ = Queen('Q2')

        self.__board_state__ = [[State.BLANK] * width for _ in range(height)]

        self.__active_player__ = p1
        self.__inactive_player__ = p2

        self.__active_player_queen__ = self.__q1__
        self.__inactive_player_queen__ = self.__q2__

        self.__last_laser_pos__ = []

    @property
    def state(self) -> Gameboard:
        return copy.deepcopy(self.__board_state__)

    def __applyMove__(self, queen_move: Space) -> Tuple[bool, Optional[Queen]]:
        row, col = queen_move

        position = self.__active_player_queen__.last_move

        self.__clearLaser__()

        if self.moveIsInBoard(position):
            self.__board_state__[position[0]][position[1]] = State.BLOCKED
            self.__createLaser__(queen_move, position)

        self.__active_player_queen__.last_move = queen_move
        self.__board_state__[row][col] = self.__active_player_queen__.token
        if not self.inactiveMoves:
            return True, self.__active_player_queen__

        self.__active_player__, self.__inactive_player__ = self.__inactive_player__, self.__active_player__
        self.__active_player_queen__, self.__inactive_player_queen__ = self.__inactive_player_queen__, self.__active_player_queen__

        return (False, None)

    def __createLaser__(self, cur_position: Space, prev_position: Space) -> None:
        cur_row, cur_col = cur_position
        prev_row, prev_col = prev_position

        if cur_row < prev_row:
            horizontal_iterator = -1
        else:
            horizontal_iterator = 1

        if cur_col < prev_col:
            vertical_iterator = -1
        else:
            vertical_iterator = 1

        if cur_col == prev_col:
            row = prev_row + horizontal_iterator
            while row != cur_row:
                self.__last_laser_pos__.append((row, cur_col))
                self.__board_state__[row][cur_col] = State.TRAIL
                row += horizontal_iterator
        elif cur_row == prev_row:
            col = prev_col + vertical_iterator
            while col != cur_col:
                self.__last_laser_pos__.append((cur_row, col))
                self.__board_state__[cur_row][col] = State.TRAIL
                col += vertical_iterator
        else:
            col, row = prev_col, prev_row
            while col != cur_col and row != cur_row:
                col += vertical_iterator
                row += horizontal_iterator

                if self.__board_state__[row][col] == State.BLANK and (row, col) != self.inactivePosition and (row, col) != (cur_row, cur_col):
                    self.__last_laser_pos__.append((row, col))
                    self.__board_state__[row][col] = State.TRAIL

    def __clearLaser__(self) -> None:
        while self.__last_laser_pos__:
            r, c = self.__last_laser_pos__.pop()
            self.__board_state__[r][c] = State.BLANK

    def copy(self):
        b = Board(self.__p1__, self.__p2__, self.width, self.height)
        b.__q1__ = self.__q1__
        b.__q2__ = self.__q2__

        b.__last_laser_pos__ = copy.deepcopy(self.__last_laser_pos__)
        b.__active_player__ = self.__active_player__
        b.__inactive_player__ = self.__inactive_player__
        b.__active_player_queen__ = copy.deepcopy(self.__active_player_queen__)
        b.__inactive_player_queen__ = copy.deepcopy(
            self.__inactive_player_queen__)
        b.__board_state__ = self.state
        return b

    def forecastMove(self, queen_move: Space) -> Tuple[Any, bool, Optional[Queen]]:
        new_board = self.copy()
        is_over, winner = new_board.__applyMove__(queen_move)
        return (new_board, is_over, winner)

    @property
    def activePlayer(self) -> Player:
        return self.__active_player__

    @property
    def inactivePlayer(self) -> Player:
        return self.__inactive_player__

    @property
    def activePlayersQueen(self) -> Queen:
        return self.__active_player_queen__

    @property
    def inactivePlayersQueen(self) -> Queen:
        return self.__inactive_player_queen__

    @property
    def inactivePosition(self) -> Space:
        return self.__inactive_player_queen__.last_move

    @property
    def activePosition(self) -> Space:
        return self.__active_player_queen__.last_move

    def getPlayerPosition(self, my_player: Player = None) -> Space:
        if my_player == self.activePlayer:
            return self.activePosition
        return self.inactivePosition

    def getOpponentPosition(self, my_player: Player = None) -> Space:
        if my_player == self.activePlayer:
            return self.inactivePosition
        return self.activePosition

    @property
    def inactiveMoves(self) -> Set[Space]:
        return self.__getMoves__(self.__inactive_player_queen__.last_move)

    @property
    def activeMoves(self) -> Set[Space]:
        return self.__getMoves__(self.__active_player_queen__.last_move)

    def __getMoves__(self, move: Space) -> Set[Space]:
        if move == (-1, -1):
            return self.firstMoves

        r, c = move
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1), (0, 1),
                      (1, -1), (1, 0), (1, 1)]

        moves = set()

        for direction in directions:
            for dist in range(1, max(self.width, self.height)):
                row = direction[0] * dist + r
                col = direction[1] * dist + c
                m = (row, col)

                if self.moveIsInBoard(m) and self.isSpotOpen(m) and m not in moves:
                    moves.add(m)
                else:
                    break
        return moves

    def getPlayerMoves(self, my_player: Player = None) -> Set[Space]:
        if my_player == self.__active_player__:
            return self.activeMoves
        return self.inactiveMoves

    def getOpponentMoves(self, my_player: Player = None) -> Set[Space]:
        if my_player == self.__active_player__:
            return self.inactiveMoves
        return self.activeMoves

    @property
    def firstMoves(self) -> Set[Space]:
        return {(i, j) for i in range(self.height) for j in range(self.width) if self.__board_state__[i][j] == State.BLANK}

    def moveIsInBoard(self, move: Space) -> bool:
        row, col = move
        return 0 <= row < self.height and 0 <= col < self.width

    def isSpotOpen(self, move: Space) -> bool:
        row, col = move
        return self.__board_state__[row][col] == State.BLANK

    def printBoard(self) -> str:
        out = '|'

        for i in range(self.width):
            out += str(i) + '|'
        out += '\n\r'
        for i in range(self.height):
            out += str(i) + '|'
            for j in range(self.width):
                if (i, j) == self.__active_player_queen__.last_move:
                    out += self.__active_player_queen__.token
                elif (i, j) == self.__inactive_player_queen__.last_move:
                    out += self.__inactive_player_queen__.token
                elif self.__board_state__[i][j] == State.BLANK:
                    out += '  '
                elif self.__board_state__[i][j] == State.TRAIL:
                    out += '- '
                else:
                    out += '><'

                out += '|'

            if i != self.height - 1:
                out += '\n\r'

        return out

    def playIsolation(self, time_limit: float = 1e6, print_moves: bool = False) -> Tuple[Queen, List[Space], str]:
        move_history = []

        def curTime() -> float:
            return float(time() * 1000)

        while True:
            game = self.copy()
            start_time = curTime()

            def timeLeft() -> float:
                return time_limit - (curTime() - start_time)

            print(timeLeft())
            if print_moves:
                print(f'\n {self.__active_player_queen__.token} turn')
                print(game.copy().printBoard())

            cur_move = self.__active_player__.move(game, timeLeft)

            if self.__active_player__ == self.__p1__:
                move_history.append([cur_move])
            else:
                move_history[-1].append(cur_move)

            if time_limit and timeLeft() <= 0:
                return self.__inactive_player_queen__, move_history, (self.__active_player_queen__.token + ' timed out.')

            if cur_move not in self.activeMoves:
                return self.__inactive_player_queen__, move_history, (self.__active_player_queen__.token + ' made an illegal move.')

            is_over, _ = self.__applyMove__(cur_move)

            if print_moves:
                print(self.copy().printBoard())

            if is_over:
                if not self.inactiveMoves:
                    return self.__active_player_queen__, move_history, (f'{self.__inactive_player_queen__.token} has no legal moves left.')
                return self.__active_player_queen__, move_history, (f'{self.__inactive_player_queen__.token} was forced off the grid.')
