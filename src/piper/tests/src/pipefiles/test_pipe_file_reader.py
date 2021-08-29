import os

from piper.config.reader import read_all_pipes


DATA = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..", "data")


def test_reader():

    pipes = read_all_pipes(os.path.join(DATA, "complexproject"))
    assert len(pipes) == 5


if __name__ == '__main__':

    test_reader()
