
class Constraints:

    def __init__(self, constraints: str):

        # Clean to remove spaces and brackets
        constraints = constraints.strip()
        if constraints.startswith("("):
            constraints = constraints[:1]
        if constraints.endswith(")"):
            constraints = constraints[:-1]

        # TODO: create single class for better handling it
        self.constraints = constraints.split(",")
