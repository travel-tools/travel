import logging
import queue
import subprocess
from queue import Queue
from threading import Thread
from typing import Optional

logger = logging.getLogger(__name__)

_STDOUT = "stdout"
_STDERR = "stderr"


class Shell:

    def __init__(self, pre_command: str = None):
        self._pre_command = f"{pre_command} && " if pre_command else ""

    def run(self, command: str, capture: bool = False, text: bool = True, cwd: str = None) -> Optional[subprocess.CompletedProcess]:
        if capture:
            return self.captured_run(command, text=text, cwd=cwd)
        else:
            self.live_run(command, text=text, cwd=cwd)

    def captured_run(self, command: str, text: bool = True, cwd: str = None):
        return subprocess.run(
            self._pre_command + command,
            check=True,
            capture_output=True,
            text=text,
            shell=True,
            cwd=cwd
        )

    def live_run(self, command: str, text: bool = True, cwd: str = None):

        output = Queue()

        def pipe(std, stream):
            # Blocking for loop: the stream will be empty only on process termination
            for line in stream:
                output.put((std, line))
            if not stream.closed:
                stream.close()

        # Instantiate the child process
        process = subprocess.Popen(
            self._pre_command + command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=text,
            shell=True,
            cwd=cwd
        )

        # Start the producers
        stdout = Thread(target=pipe, args=(_STDOUT, process.stdout))
        stdout.start()
        stderr = Thread(target=pipe, args=(_STDERR, process.stderr))
        stderr.start()

        # Be the consumer
        outcome = None
        while outcome is None:

            try:

                try:
                    # Get a line, waiting at most one second (cannot be less)
                    line = output.get(timeout=0.2)
                except queue.Empty:
                    # Nothing to do
                    pass
                else:
                    # Print that line
                    std, msg = line
                    msg = msg.rstrip("\r\n") if text else msg
                    if std == _STDOUT:
                        logger.info(msg)
                    else:
                        logger.error(msg)
                finally:
                    # Check if the process has ended
                    outcome = process.poll()

            except KeyboardInterrupt:

                process.kill()
                outcome = -9

        # Release resources (if possible)
        stdout.join(1)
        stderr.join(1)
        if outcome != 0:
            exit(outcome)
        return outcome
