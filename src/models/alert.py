import uuid
from typing import Dict
from dataclasses import dataclass, field
from src.models.item import Item
from src.models.model import Model
from src.models.user import User
from src.libs.mailgun import Mailgun

__author__ = 'benbrown'


@dataclass(eq=False)
class Alert(Model):
    collection: str = field(init=False, default="alerts")
    name: str
    item_id: str
    price_limit: float
    user_email: str
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def __post_init__(self):
        self.item = Item.get_by_id(self.item_id)
        self.user = User.find_by_email(self.user_email)

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "name": self.name,
            "item_id": self.item_id,
            "price_limit": self.price_limit,
            "user_email": self.user_email
        }

    def load_item_price(self) -> float:
        self.item.load_price()
        return self.item.price

    def notify_if_price_reached(self):
        if self.item.price < self.price_limit:
            print(f"Item {self.item} has reached a price under {self.price_limit}, latest price is {self.item.price}.")
            Mailgun.send_mail(
                [self.user_email],
                f'Notification for {self.name}',
                f'Your alert {self.name} has reached a price under {self.price_limit}. Latest price: {self.item.price}. Go to this address to check your item: {self.item.url}.',
                f'<p>Your alert {self.name} has reached a price under {self.price_limit}.</p><p>Latest price: {self.item.price}</p><p>Click <a href={self.item.url}>here</a> to purchase your item.</p>'
            )
