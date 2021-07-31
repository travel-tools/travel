import os

from piper.config.reader import read_pipe_files


DATA = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "data")


def test_reader():

    pipes = read_pipe_files(os.path.join(DATA, "complexproject"))
    assert len(pipes) == 4


if __name__ == '__main__':

    test_reader()
