class RiskManager:
    def __init__(self, capital: float = 500000):
        self.capital = capital

    def validate(self, signal, quantity: int = 1):
        if signal is None:
            return False, 'No signal'

        if quantity <= 0:
            return False, 'Invalid quantity'

        return True, 'Risk checks passed'
