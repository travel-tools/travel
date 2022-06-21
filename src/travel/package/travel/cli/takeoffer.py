import os

from travel.config.reader import parse_bags
from travel.custom.tasks import performer
from travel.tools.python import main_python


def take_off(context: str, command: str, target: str = None):

    bag, _ = parse_bags(context, target=target)

    # Pre-takeoff
    performer.perform_tasks("takeoff", "pre", bag)

    # Instead of takeoff
    skip = performer.perform_tasks("takeoff", "instead", bag)

    # Main takeoff
    if not skip:
        complete_command = ' '.join(command)
        dist = os.path.join(bag.dist_folder, '*')
        main_python.run(f"-m twine upload {complete_command} {dist}")

    # Post-takeoff
    performer.perform_tasks("takeoff", "post", bag)
