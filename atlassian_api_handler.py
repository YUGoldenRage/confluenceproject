from atlassian import Confluence
from urllib.error import HTTPError
import requests
import json


def token_binding(host, token):
    """
    Create Confluence Object.
    :param host:
    :param token:
    :return:
    """
    confluence = Confluence(
        url=host,
        token=token)

    return confluence


def validate_user(confluence, admin):
    """
    Confirms The User Existence.
    :param confluence:
    :param admin:
    :return:
    """
    try:
        print(admin)
        confluence.get_user_details_by_username(admin)
        print("hi")
        return True
    except:
        print("Failed")
        return False



def user_input(confluence, space_name, space_key, space_admin):
    """
    Takes Input From The User.
    :param confluence:
    :return:
    """
    validate_user(space_admin)


    return name, key, admin


def start_creation(host, confluence, space_name, space_key, space_admin):
    """
    Creates The Space.
    :param confluence:
    :return:
    """
    if not validate_user(confluence, space_admin):
        return False, "The Admin You Entered Does Not Exist"

    try:
        print("space key: " + space_key)
        confluence.create_space(space_key=space_key, space_name=space_name)
        linked = f"{host}/display/{space_key}/{space_name.replace(' ','+')}+Home"

        return True, f'Your Space Was Created Successfully.It Can Be Accessed From The Link: {linked}'

    except Exception as e:
        return False, "The Space Key You Entered Is Taken."



def set_admin(host, access_token, admin, key):
    """
    Grants All Privileges To The User Inserted Before And Removes VIEW Permissions To All Users.
    :param host:
    :param access_token:
    :param admin:
    :param key:
    :return:
    """
    url = f"{host}/rpc/json-rpc/confluenceservice-v2/addPermissionsToSpace"
    PERMSARR = ["VIEWSPACE", "REMOVEOWNCONTENT", "COMMENT", "EDITSPACE", "SETSPACEPERMISSIONS", "REMOVEPAGE",
                "REMOVECOMMENT", "REMOVEBLOG", "CREATEATTACHMENT", "REMOVEATTACHMENT", "EDITBLOG", "EXPORTSPACE",
                "REMOVEMAIL", "SETPAGEPERMISSIONS"]

    requestArray = json.dumps([PERMSARR, admin, key])
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    requests.request(
        "POST",
        url,
        data=requestArray,
        headers=headers
    )

    url = f"{host}/rpc/json-rpc/confluenceservice-v2/removePermissionFromSpace"

    requestArray = json.dumps(["VIEWSPACE", "confluence-users", key])
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    print("here!!!!!")
    response = requests.request(
        "POST",
        url,
        data=requestArray,
        headers=headers
    )
    print(response)

    return response


def validate_credentials(user,password):
    if user == "user" and password == "pass":
        return True
    return False




def start_confluence_api(user, password, space_name, space_key, space_admin):
    if not validate_credentials(user,password):
        return False, "You're Username Or Password Are Incorrect"

    host = "http://localhost:8090"
    token = "Njk0MTM3MDAwNDIzOsAlqTjAMlkxsiwdzXgxvHVxNge7"
    confluence = token_binding(host, token)
    status, error_str = start_creation(host, confluence, space_name, space_key, space_admin)
    set_admin(host, token, space_admin, space_key)
    return status, error_str
