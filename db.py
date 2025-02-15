from tinydb import TinyDB

tindb = TinyDB('db.json', indent = 4)

def get_models():
    models = tindb.tables()
    return models

def get_one_model(model: str):
    if model in get_models():
        one_model_all = tindb.table(model)
        return one_model_all.all()
    else:
        return []

