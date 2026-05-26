from fastapi import FastAPI

app = FastAPI(title='SENSEX Options Algo API')

@app.get('/health')
def health():
    return {'status': 'ok'}
