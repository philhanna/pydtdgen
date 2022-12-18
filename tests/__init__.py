from pathlib import Path
import sys
import tempfile
from contextlib import contextmanager

this_file = Path(__file__)
tests_dir = this_file.parent
project_root = tests_dir.parent
testdata = project_root.joinpath("testdata")
tmp = tempfile.gettempdir()


# redirect stdout technique from https://www.python.org/dev/peps/pep-0343/

@contextmanager
def stdout_redirected(new_stdout):
    save_stdout = sys.stdout
    sys.stdout = new_stdout
    try:
        yield None
    finally:
        sys.stdout = save_stdout


@contextmanager
def stderr_redirected(new_stderr):
    save_stderr = sys.stderr
    sys.stderr = new_stderr
    try:
        yield None
    finally:
        sys.stderr = save_stderr


@contextmanager
def stdin_redirected(new_stdin):
    save_stdin = sys.stdin
    sys.stdin = new_stdin
    try:
        yield None
    finally:
        sys.stdin = save_stdin


__all__ = [
    'tmp',
    'project_root',
    'testdata',
    'stdout_redirected',
    'stderr_redirected',
    'stdin_redirected',
]
