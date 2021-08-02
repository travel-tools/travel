from piper.cli.setupper import setup


def run(pipe_location: str, script: str = None):

    # Setup the pipes and dependencies
    setup(pipe_location)

    # Run the code
    pass
