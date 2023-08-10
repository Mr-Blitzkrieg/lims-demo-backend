def update_db_object(db_object:object, update_data:dict) -> object:
    for attribute, value in update_data.items():
        if hasattr(db_object,attribute):
            setattr(db_object, attribute, value)
    db_object.save()
    return db_object
