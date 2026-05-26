class Backtester:
    def __init__(self):
        self.results = []

    def run(self, historical_data):
        return {
            'trades': 0,
            'win_rate': 0,
            'sharpe_ratio': 0,
            'max_drawdown': 0,
        }
