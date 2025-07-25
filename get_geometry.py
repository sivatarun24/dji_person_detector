from arcgis.gis import GIS
from arcgis.features import FeatureLayer

# Connect to ArcGIS Online
gis = GIS("https://intern-hackathon.maps.arcgis.com", "<add-username>", "<add-password>")

# Your feature layer
layer_url = "https://services8.arcgis.com/LLNIdHmmdjO2qQ5q/arcgis/rest/services/person_location/FeatureServer/0"
layer = FeatureLayer(layer_url)

# Query all features (with geometry in WGS84)
features = layer.query(
    where="1=1",
    out_fields="*",
    return_geometry=True,
    out_sr=4326,
    result_record_count=-1  # ❗ ensures no pagination limit
).features

# Loop through and print each
for f in features:
    attrs = f.attributes
    geom = f.geometry
    print(f"OBJECTID: {attrs['OBJECTID']}, Name: {attrs.get('Name')}, X: {geom['x']}, Y: {geom['y']}")
