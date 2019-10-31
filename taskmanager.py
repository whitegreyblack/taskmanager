# taskmanager.py

"""
    Task manager (tm for short) handles reading in a formatted task file and
    creates a view based on task statuses using curses library

    Format: id, task_name, status
    Status:
        0 = to-do
        1 = in-prog
        2 = done
"""

import sys
import curses
from dataclasses import dataclass, field


@dataclass
class Task:
    name: str
    status: int

@dataclass
class TaskBuckets:
    todo: list = field(default_factory=list)
    prog: list = field(default_factory=list)
    done: list = field(default_factory=list)

def build_tasks(tasks_file_path):
    with open(tasks_file_path) as f:
        tasks = [ Task(*line.split(", ")) for line in f.readlines() ]
    return tasks

def sort_tasks(tasks):
    buckets = TaskBuckets()
    for task in tasks:
        if int(task.status) == 0:
            buckets.todo.append(task)
        elif int(task.status) == 1:
            buckets.prog.append(task)
        elif int(task.status) == 2:
            buckets.done.append(task)
        else:
            raise Exception(f"Invalid bucket value {task.status}")
    return buckets

def draw_titles(board):
    _, board_width = board.getmaxyx()
    bucket_width = board_width // 3
    title_width = bucket_width - 2    
    for i, title in enumerate(("TODO", "In Progress", "Completed")):
        x = bucket_width * i
        board.addstr(1, x+1, title[:title_width])

def draw_grid(board):
    _, board_width = board.getmaxyx()
    board.hline(2, 1, curses.ACS_HLINE, board_width-2)

def draw_tasks(board, buckets):
    indexes = [0, 0, 0]
    _, board_width = board.getmaxyx()
    bucket_width = board_width // 3
    title_width = bucket_width - 2 
    for i, bucket in enumerate((buckets.todo, buckets.prog, buckets.done)):
        x = bucket_width * i
        for j, task in enumerate(bucket):
            board.addstr(3+j, x+1, task.name)

def draw_board(board, buckets):
    board.border()
    draw_titles(board)
    draw_grid(board) 
    draw_tasks(board, buckets)

def main(screen, tasks_file_path):
    curses.curs_set(0)
    tasks = build_tasks(tasks_file_path)
    buckets = sort_tasks(tasks)
    
    while True:
        draw_board(screen, buckets)
        char = screen.getch()
        if char == 27:
            break

if __name__ == '__main__':
    if len(sys.argv) == 1:
        tasks_file_path = "./tasks.txt"
    elif len(sys.argv) == 2:
        tasks_file_path = sys.argv[1]
    else:
        exit("Invalid argument length")
    curses.wrapper(main, tasks_file_path)
