from piper.cli.setupper import Setupper


def run(pipe_location: str, script: str = None):

    # Setup the pipes and dependencies
    Setupper().manage(pipe_location)

    # Run the code
    pass
