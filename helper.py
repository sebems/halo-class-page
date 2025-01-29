import pandas as pd
import requests, json

### API CALL for Token

base_URL = "https://halo.calvin.edu/api"
auth_URL = "https://halo.calvin.edu/auth/token?tenant=calvinuni"
asset_URL = base_URL + "/asset"
CLIENT_ID = ""
CLIENT_SECRET = ""
ASSET_GROUP_ID = 103 # asset group id for classrooms

data = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "grant_type": "client_credentials",
    "scope": "read:assets edit:assets"
}

building_codes = {
    "Arena Complex Classrooms": "HC",
    "CFAC Classrooms": "CF",
    "Chapel Classrooms": "CP",
    "Commons Annex Classrooms": "CA",
    "DeVos Classrooms": "DC",
    "DeVries Hall Classrooms": "DH",
    "Engineering Building Classrooms": "EB",
    "Hiemenga Hall Classrooms": "HH",
    "North Hall Classrooms": "NH",
    "Science Building Classrooms": "SB",
    "Spoelhof University Center Classrooms": "SC"
}

def getToken():
    """
    Gets API Token for session. This has read and edit access to assets in Halo ITSM

        @return:
            token: str -- API Token
    """
    response = requests.post(auth_URL, data=data)
    return response.json()["access_token"] if response.ok else ''


def getClassroomAssets(token):
    """
    Gets the list of Classrooms from Halo in Dictionary variable

        @returns:
            classroom_json: dict
    """

    try:
        if len(token) > 0:
            headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
            query = "?assetgroup_id={}".format(ASSET_GROUP_ID)

            response = requests.get(url=asset_URL+query, headers=headers)
            asset_count = response.json()["record_count"]
            classroom_json = response.json()["assets"]

            if asset_count != 0:
                return classroom_json
            else:
                return("No Classrooms in the Database")
        else:
            raise Exception
    except Exception as err:
        print(err, "Token is empty")

def getClassRoomsCondensed(token):
    """
    Gets the list of Classrooms Assets from Halo in a Codensed Dictionary variable

        @returns:
            modi_classes: dict
    """

    modi_classes = {
        "Arena Complex Classrooms": [],
        "CFAC Classrooms": [],
        "Chapel Classrooms": [],
        "Commons Annex Classrooms": [],
        "DeVos Classrooms": [],
        "DeVries Hall Classrooms": [],
        "Engineering Building Classrooms": [],
        "Hiemenga Hall Classrooms": [],
        "North Hall Classrooms": [],
        "Science Building Classrooms": [],
        "Spoelhof University Center Classrooms": []
    }

    try:
        if len(token) > 0:
            headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
            query = "?assetgroup_id={}".format(ASSET_GROUP_ID)

            response = requests.get(url=asset_URL+query, headers=headers)
            asset_count = response.json()["record_count"]
            classroom_json = response.json()["assets"]

            for classroom in classroom_json:
                halo_building_name = classroom["assettype_name"]
                room_name = classroom["inventory_number"]
                room_id = classroom["id"]
                building_code = building_codes[halo_building_name]

                modi_classes[halo_building_name].append({
                    room_id,
                    building_code,
                    room_name
                })

            if asset_count != 0:
                return modi_classes
            else:
                return("No Classrooms in the Database")
        else:
                raise Exception
    except Exception as err:
        print(err, "Token is empty")
