import re
import requests
import uuid
from typing import Dict
from dataclasses import dataclass, field
from bs4 import BeautifulSoup
from src.models.model import Model

__author__ = 'benbrown'


@dataclass(eq=False)
class Item(Model):
    collection: str = field(init=False, default="items")
    url: str
    tag_name: str
    # Added three "query" fields to accommodate source pages breaking up price into separate pieces
    # If nothing is passed in by the user, query2 and query 3 will default to "." and "99", respectively
    # query1 = currency (XXX of $XXX.CC)
    # query2 = currency percentile separator (. of $XXX.CC)
    # query3 = currency remainder (CC of $XXX.CC)
    query1: Dict
    query2: Dict = field(default=None)
    query3: Dict = field(default=None)
    price: float = field(default=None)
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def __repr__(self):
        return f"<Item {self.url}>"

    def load_price(self) -> float:
        response = requests.get(self.url)
        content = response.content
        soup = BeautifulSoup(content, "html.parser")
        element1 = soup.find(self.tag_name, self.query1)
        # If query2 and/or query 3 are not populated, use defaults
        # Otherwise, strip found values of any extra characters
        if self.query2 is not None:
            element2 = f'{soup.find(self.tag_name, self.query2).text.strip()}'
        else:
            element2 = "."
        if self.query3 is not None:
            element3 = f'{soup.find(self.tag_name, self.query3).text.strip()}'
        else:
            element3 = "99"
        # Construct full price
        string_price = f'{element1.text.strip()}{element2}{element3}'

        pattern = re.compile(r"(\d+,?\d*,?\d*\.\d\d)")
        match = pattern.search(string_price)
        found_price = match.group(1)
        without_commas = found_price.replace(",", "")
        self.price = float(without_commas)
        return self.price

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "url": self.url,
            "tag_name": self.tag_name,
            "price": self.price,
            "query1": self.query1,
            "query2": self.query2,
            "query3": self.query3
        }
