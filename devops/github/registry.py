import os
from enum import Enum

import requests
import argparse


class GitHubRegistry:

    def __init__(self, organization, type, personal_access_token):
        self._url = f"https://api.github.com/orgs/{organization}/packages/{type}"
        self._auth = personal_access_token

    def _call(self, *args, **kwargs):
        response = requests.request(*args, **{**kwargs, "auth": self._auth})
        response.raise_for_status()
        return response

    def get_versions(self, artifact):
        return self._call(
            method="GET",
            url=self._url + f"/{artifact}/versions"
        ).json()

    def delete(self, artifact, version):
        return self._call(
            method="DELETE",
            url=self._url + f"/{artifact}/versions/{version}"
        )

    def delete_all_except_last(self, artifact, n):
        versions = self.get_versions(artifact)
        to_delete = sorted(versions, key=lambda v: v["updated_at"])[:-n]
        for version in to_delete:
            print(f"Deleting {artifact}:{version['tags']}")
            self.delete(artifact, version["id"])


class Action(str, Enum):

    DELETE_ALL_EXCEPT_LAST = "delete-all-except-last"


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact")
    parser.add_argument("--type", default="container")
    parser.add_argument("--action", choices=[a for a in Action])
    args, _ = parser.parse_known_args()
    action = args.action
    artifact = args.artifact

    registry = GitHubRegistry(
        organization="piper-tools",
        type=args.type,
        personal_access_token=("federicopugliese", os.environ["REGISTRY_PAT"])
    )

    if action == Action.DELETE_ALL_EXCEPT_LAST:

        parser = argparse.ArgumentParser()
        parser.add_argument("--keep", type=int)
        args, _ = parser.parse_known_args()

        registry.delete_all_except_last(artifact, int(args.keep))

