from server import app


@app.get('/')
def read_root():
    return {'game': 'whist'}
