from typing_extensions import Dict, Tuple, Union
import string
import random

def generate_slug() -> str:
    """
    generates a 6 character slug for the shortened link
    characters consist of a-z, A-Z, and 0-9
    ! DOES NOT CHECK FOR DUPLICATE SLUGS
    * 62^6 possible links should be enough
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=6))

def check_create_body(data: Dict) -> Tuple[Dict, Union[str, None]]:
    """
    checks on the server if data has the necessary parameters
    also checks all the parameters are valid
    return structure: [data, err]
    * don't need to check created_at since that's autofilled by the db
    * if id is none, use generate slug
    """
    # required
    valid_data = {}
    id = data.get("id")
    if (id == None):
        valid_data["id"] = generate_slug()
    elif (isinstance(id, str) and len(id) <= 255):
        valid_data["id"] = id
    else:
        return {}, "[INVALID] id: should be a string less than 256 characters, or null to autogenerate the id"
    link = data.get("link")
    if (isinstance(link, str)):
        valid_data["link"] = link
    else:
        return {}, "[INVALID] link: should be a string"
    # optional
    # TODO: finish checks for optional parameters
    expires_at = data.get("expires_at")
    password = data.get("password")
    auth = data.get("auth")
    return valid_data, None
