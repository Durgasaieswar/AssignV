from xml.dom import minidom

import jmespath
import requests
from flask import Flask, request

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False


def xml_response(x, y, addr):
    """To create response in xml format

    Args:
        x (float): Latitude
        y (float): Longitude
        addr (str): Location

    Returns:
        _pxml(str): xml format response
    """
    _xml = minidom.Document()
    main_tag = _xml.createElement('root')
    _xml.appendChild(main_tag)

    addr_tag = _xml.createElement('address')
    main_tag.appendChild(addr_tag)
    addr_tag.appendChild(_xml.createTextNode(str(addr)))
    
    coord_tag = _xml.createElement('coordinates')
    main_tag.appendChild(coord_tag)
    
    lat_tag = _xml.createElement('lat')
    coord_tag.appendChild(lat_tag)
    lat_tag.appendChild(_xml.createTextNode(str(x)))
    
    lng_tag = _xml.createElement('lng')
    coord_tag.appendChild(lng_tag)
    lng_tag.appendChild(_xml.createTextNode(str(y)))

    _pxml = _xml.toprettyxml(encoding="utf-8", indent="\t")

    return _pxml


@app.route('/getAddressDetails', methods=['POST'])
def addr_details():

    """API to get the latitude & longitude details of given
        address

    Returns:
        response(json/xml): Longitude & latitude details
    """

    # Receive payload
    payload = request.json
    
    # Call Google API with API KEY
    api_link = "https://maps.googleapis.com/maps/api/geocode/json"

    kwargs = {
        "address": payload["address"],
        "key": API_KEY
    }
    g_res = requests.get(api_link, params=kwargs)
    g_json = g_res.json()
    
    # Get latitude and longitude    
    latitude = "results[0].geometry.location.lat"
    longitude = "results[0].geometry.location.lng"
    lat = round(jmespath.search(latitude, g_json), 6)
    lng = round(jmespath.search(longitude, g_json), 6)

    # Create response
    response = {
        "coordinates": {
            "lat": lat,
            "lng": lng
        },
        "address": payload["address"]
    }
    if payload["output_format"] == "xml":
        response = xml_response(lat, lng, payload["address"])

    return response


if __name__ == "__main__":
    
    app.run()
