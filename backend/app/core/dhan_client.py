import logging
from dhanhq import dhanhq

logger = logging.getLogger(__name__)


class DhanClient:
    def __init__(self, client_id: str, access_token: str):
        self.client = dhanhq(client_id, access_token)

    def get_funds(self):
        return self.client.get_fund_limits()

    def get_positions(self):
        return self.client.get_positions()

    def get_order_book(self):
        return self.client.get_order_list()
