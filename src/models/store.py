import uuid
import re
from typing import Dict
from dataclasses import dataclass, field
from src.models.model import Model

__author__ = 'benbrown'


@dataclass(eq=False)
class Store(Model):
    collection: str = field(init=False, default="stores")
    name: str
    url_prefix: str
    tag_name: str
    # Added three "query" fields to accommodate source pages breaking up price into separate pieces
    # If nothing is passed in by the user, query2 and query 3 will default to "." and "99", respectively
    # query1 = currency (XXX of $XXX.CC)
    # query2 = currency percentile separator (. of $XXX.CC)
    # query3 = currency remainder (CC of $XXX.CC)
    query1: Dict
    query2: Dict = field(default=None)
    query3: Dict = field(default=None)
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "name": self.name,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "query1": self.query1,
            "query2": self.query2,
            "query3": self.query3
        }

    @classmethod
    def get_by_name(cls, store_name: str) -> "Store":
        return cls.find_one_by("name", store_name)

    @classmethod
    def get_by_url_prefix(cls, url_prefix: str) -> "Store":
        url_regex = {"$regex": "^{}".format(url_prefix)}
        return cls.find_one_by("url_prefix", url_regex)

    @classmethod
    def find_by_url(cls, url: str) -> "Store":
        pattern = re.compile(r"(https?://.*?/)")
        match = pattern.search(url)
        url_prefix = match.group(1)
        return cls.get_by_url_prefix(url_prefix)
