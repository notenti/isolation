from time import time
from enum import Enum
import copy
from typing import List, Set, Tuple, Union, Optional, Any
from dataclasses import dataclass


class State(Enum):
    """Representation of space state."""
    BLANK = ' '
    BLOCKED = 'X'
    TRAIL = 'O'
    Q1 = 'Q1'
    Q2 = 'Q2'


Space = Tuple[int, int]


@dataclass
class Queen:
    """Represents Queen."""
    token: State
    last_move: Space = (-1, -1)


Gameboard = List[List[Union[State]]]


class Board:
    def __init__(self, board_repres: str) -> None:
        self.width = 7
        self.height = 7

        self.__board_repres__ = board_repres

        self.__p1__ = 'me'
        self.__p2__ = 'them'

        self.__q1__ = Queen(State.Q1)
        self.__q2__ = Queen(State.Q2)

        opp_last_queen_start = board_repres.index('O')
        ai_last_queen_start = board_repres.index('A')
        x_start = board_repres.index('X')
        trail_start = board_repres.index('T')

        opp_queen_walker = opp_last_queen_start + 1
        while opp_queen_walker != ai_last_queen_start:
            opp_queen_loc = (int(board_repres[opp_queen_walker]), int(board_repres[opp_queen_walker + 1]))
            opp_queen_walker += 2
            self.__q2__.last_move = opp_queen_loc

        ai_queen_walker = ai_last_queen_start + 1
        while ai_queen_walker != x_start:
            ai_queen_loc = (int(board_repres[ai_queen_walker]), int(board_repres[ai_queen_walker + 1]))
            ai_queen_walker += 2
            self.__q1__.last_move = ai_queen_loc

        x_walker = x_start + 1
        spaces_occupied_x = []
        while x_walker != trail_start:
            x_loc = (int(board_repres[x_walker]), int(board_repres[x_walker + 1]))
            spaces_occupied_x.append(x_loc)
            x_walker += 2

        trail_walker = trail_start + 1
        spaces_occupied_trail = []
        while trail_walker < len(self.__board_repres__) :
            trail_loc = (int(board_repres[trail_walker]), int(board_repres[trail_walker + 1]))
            spaces_occupied_trail.append(trail_loc)
            trail_walker += 2


        self.__board_state__ = [[State.BLANK] * self.width for _ in range(self.height)]

        if self.__q1__.last_move != (-1, -1):
            r, c = self.__q1__.last_move
            self.__board_state__[r][c] = State.Q1

        if self.__q2__.last_move != (-1, -1):
            r, c = self.__q2__.last_move
            self.__board_state__[r][c] = State.Q2

        while spaces_occupied_x:
            r, c = spaces_occupied_x.pop()
            self.__board_state__[r][c] = State.BLOCKED

        while spaces_occupied_trail:
            r, c = spaces_occupied_trail.pop()
            self.__board_state__[r][c] = State.TRAIL



        self.__active_player__ = self.__p1__
        self.__inactive_player__ = self.__p2__

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
        b = Board(self.__board_repres__)
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
    def activePlayer(self) -> str:
        return self.__active_player__

    @property
    def inactivePlayer(self) -> str:
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

    def getPlayerMoves(self, player: str) -> Set[Space]:
        if player == self.__active_player__:
            return self.activeMoves
        return self.inactiveMoves

    def getOpponentMoves(self, player: str) -> Set[Space]:
        if player == self.__active_player__:
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
