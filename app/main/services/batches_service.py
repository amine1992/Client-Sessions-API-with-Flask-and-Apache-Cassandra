from ..persistance import db

def get_batch_data(batch_data):
    db.import_from_source(batch_data, is_ttl=True)