import curses
import random
import itertools
import time
import argparse

# Constant abstractions for X and Y coordinates
X, Y = 0, 1


def get_board_points(dims):
    '''returns all points on a dims.X*dims.Y board'''
    return list(itertools.product(range(dims[X]), range(dims[Y])))


def initial_config(dims, num_points):
    '''Returns the initial set of points to the board'''
    return set(random.sample(get_board_points(dims), num_points))


def get_neighbors(p):
    '''return the set of eight neighbors for a point p'''
    all_neighbors = set(
        map(lambda p_shift: (p[X] + p_shift[X], p[Y] + p_shift[Y]),
            itertools.product([1, 0, -1], repeat=2)))

    return all_neighbors - {p}


def num_living_neighbors(p, board):
    '''return the number of living neighbors for point p'''
    return len(get_neighbors(p) & board)


def rules(p, board):
    if p in board:
        return True if num_living_neighbors(p, board) in {2, 3} else False
    else:
        return True if num_living_neighbors(p, board) == 3 else False


def step(board, dims):
    '''return the next generation of points for a given board'''
    board = set(filter(lambda p: rules(p, board), get_board_points(dims)))
    return board


def draw_board(stdscr, board, padding_x, padding_y):
    '''draws a board with the map function'''
    list(
        map(lambda p: stdscr.addstr(padding_y + p[Y], padding_x + p[X], 'O'),
            board))


def draw_frame(stdscr, x_range, y_range):
    '''draws a frame for the baord'''
    top_line = {(x, y_range[0]) for x in range(*x_range)}
    bottom_line = {(x, y_range[1]) for x in range(x_range[0], x_range[1] + 1)}
    right_line = {(x_range[0], y) for y in range(*y_range)}
    left_line = {(x_range[1], y) for y in range(*y_range)}

    frame = left_line | right_line | top_line | bottom_line
    list(map(lambda p: stdscr.addstr(p[Y], p[X], '#'), frame))


def draw_label(stdscr, h, padding_x, padding_y, cur_gen, num_gen):
    stdscr.addstr(h - padding_y + 2, padding_x, f"generation {cur_gen.zfill(len(num_gen))}/{num_gen}")


def main(stdscr, generations, num_start_points, time_delay):
    '''Calculates padding and runs the game of life'''
    curses.curs_set(0)

    (w, h) = (curses.COLS, curses.LINES)

    padding_x = 5
    padding_y = 5

    dims = (w - 2 * padding_x, h - 2 * padding_y)
    assert (dims[X] * dims[Y] >= args.num_start_points)

    board = initial_config(dims, num_start_points)

    for i in range(generations+1):
        draw_frame(stdscr, (padding_x - 1, w - padding_x + 1),
                   (padding_y - 1, h - padding_y + 1))
        draw_board(stdscr, board, padding_x, padding_y)
        draw_label(stdscr, h, padding_x, padding_y, str(i), str(generations))
        stdscr.refresh()
        time.sleep(time_delay)
        board = step(board, dims)
        stdscr.clear()


if __name__ == "__main__":
    parser = argparse.ArgumentParser("play the game of life")
    parser.add_argument("-n",
                        "--num-start-points",
                        type=int,
                        default=200,
                        help="how many starting points")
    parser.add_argument("-g",
                        "--generations",
                        type=int,
                        default=20,
                        help="how many generations to run the game of life")
    parser.add_argument("-t",
                        "--time-delay",
                        type=int,
                        default=1,
                        help="how many seconds to wait between generations")
    args = parser.parse_args()

    curses.wrapper(main, args.generations, args.num_start_points,
                   args.time_delay)
