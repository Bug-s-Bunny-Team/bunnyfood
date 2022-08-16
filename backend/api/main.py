from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def read_root():
    return {'Bunny': 'Food'}


@app.get('/locations')
def read_locations():
    return [
        {
            'id': 1,
            'name': 'Panineria veneta',
            'description': 'Una panineria random'
        }
    ]


@app.get('/profiles')
def read_profiles():
    return [
        {
            'id': 1,
            'username': 'someone'
        }
    ]
