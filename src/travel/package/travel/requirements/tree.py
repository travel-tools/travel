from typing import List

import importlib_metadata
from travel.requirements.requirement import Requirement


_EXTRA = " extra == "


class RequirementTree:

    # This works because of a complete visit. Extras won't work otherwise.

    def __init__(self, requirements: List[str]):
        parsed_reqs = [Requirement(r) for r in requirements]
        self._extras = {r.name: r.extras for r in parsed_reqs}
        self._flat_requirements = [r.name for r in self._find_recursively(parsed_reqs)]

    def get_flat_requirements(self):
        return self._flat_requirements

    def _belonging_extra(self, text_requirement):
        return text_requirement.split(_EXTRA)[1].replace("'", "")

    def _get_implicit_requirements(self, requirement: Requirement) -> List[Requirement]:
        all_requirements = importlib_metadata.distribution(requirement.name).requires or []
        all_parsed_requirements = {r: Requirement(r) for r in all_requirements}
        considered = [
            all_parsed_requirements[text_requirement]  # The real requierment object
            for text_requirement in all_requirements
            if (_EXTRA not in text_requirement  # it is not an extra
                or  # or the belonging extra is required
                 (
                    all_parsed_requirements[text_requirement] in self._extras
                    and
                    self._belonging_extra(text_requirement) in self._extras[all_parsed_requirements[text_requirement]].name
                 )
                )
        ]
        return considered

    def _find_recursively(self, explicit_requirements: List[Requirement]) -> List[Requirement]:
        # Get the implicit requirements, needed by these requirements
        implicit_requirements = []
        for r in explicit_requirements:
            print(r.name)
            for implicit in self._get_implicit_requirements(r):
                # Append it
                implicit_requirements.append(implicit)
                # Remember the extra
                for extra in implicit.extras:
                    extra_list = self._extras.get(implicit, [])
                    extra_list.append(extra)
                    self._extras[implicit] = extra_list

        # If any implicit, recursively get their implicit ones; else return it simply
        if implicit_requirements:
            requires = explicit_requirements + self._find_recursively(implicit_requirements)
        else:
            requires = explicit_requirements
        return requires


if __name__ == '__main__':

    print(RequirementTree(["cookiecutter"]).get_flat_requirements())
