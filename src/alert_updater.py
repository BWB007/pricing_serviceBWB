from src.models.alert import Alert
from dotenv import load_dotenv

load_dotenv()

__author__ = 'benbrown'

alerts = Alert.all()

for alert in alerts:
    alert.load_item_price()
    alert.notify_if_price_reached()

if not alerts:
    print("No alerts yet! Add an item and an alert to begin!")
