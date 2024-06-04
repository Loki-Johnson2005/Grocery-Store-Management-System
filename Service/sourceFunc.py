from model import source
from Service import inputValidator
from Database import crud


def add_source(s_name, s_location, s_type, s_capacity, s_status, s_water_level):
    # Check if compulsory fields are not empty/blank (s_name, s_location, s_type, s_capacity, s_status,
    # s_water_level, s_moderator_1)
    if any(not field.strip() for field in
           (s_name, s_location, s_type, s_capacity, s_status, s_water_level)):
        return "Please fill in all required fields"

    # Check if fields contain valid input type (double or integer)
    if not inputValidator.is_string_valid_numeric_input(s_capacity, s_water_level):
        return "Invalid input for numeric fields"
    # Create a new source object and add all the data in the required fields
    new_source = source.Source()
    new_source.name = s_name
    new_source.location = s_location
    new_source.type = s_type
    new_source.capacity = float(s_capacity)
    new_source.status = s_status
    new_source.water_level = float(s_water_level)

    # Persist the new source and quality objects to the database
    try:
        crud.add(new_source)
        return new_source
    except Exception as e:
        return str(e)


def get_all_sources():
    return crud.find_all(source.Source)


def get_source_by_name(source_name):
    return crud.find_by("name", source_name, source.Source)


def get_source_id_by_name(source_name):
    new_source = crud.find_by("name", source_name, source.Source)
    return new_source.id
