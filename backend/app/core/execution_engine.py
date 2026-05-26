class ExecutionEngine:
    def __init__(self, dhan_client, mode='paper'):
        self.dhan_client = dhan_client
        self.mode = mode

    def execute(self, signal, quantity: int):
        if self.mode == 'paper':
            return {
                'mode': 'paper',
                'status': 'simulated',
                'signal': signal.strategy,
                'quantity': quantity,
            }

        return {
            'mode': 'live',
            'status': 'submitted'
        }
