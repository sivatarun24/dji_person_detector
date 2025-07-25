from arcgis_client import ArcGISClient

client = ArcGISClient(
    username="<add-username>", 
    password="<add-password>",
    org_url="https://intern-hackathon.maps.arcgis.com",
    layer_url="https://services8.arcgis.com/LLNIdHmmdjO2qQ5q/arcgis/rest/services/person_location/FeatureServer/0"
)

# Push location
client.push_location(34.0572, -117.1956, image_path="output/frame_10.jpg")

# Or fetch all
client.get_all_locations()
