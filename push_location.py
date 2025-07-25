from arcgis.gis import GIS
from arcgis.features import FeatureLayer

gis = GIS("https://intern-hackathon.maps.arcgis.com", "<add-username>", "<add-password>")
feature_layer_url = "https://services8.arcgis.com/LLNIdHmmdjO2qQ5q/arcgis/rest/services/person_location/FeatureServer/0"
layer = FeatureLayer(feature_layer_url)

def push_person_location(lat, lon, image_path, name="Person", status="Detected"):
    new_feature = {
        "geometry": {
            "x": lon,
            "y": lat,
            "spatialReference": {"wkid": 4326}
        },
        "attributes": {
            "Name": name,
            "Status": status,
            "Latitude": lat,
            "Longitude": lon
        }
    }

    try:
        result = layer.edit_features(adds=[new_feature])

        if result.get("addResults") and result["addResults"][0]["success"]:
            object_id = result["addResults"][0]["objectId"]
            print(f"✅ Feature added: ({lat}, {lon}) with objectId={object_id}")

            # Attach image
            if image_path and os.path.exists(image_path):
                with open(image_path, 'rb') as img_file:
                    attachment_result = layer.attachments.add(
                        object_id=object_id,
                        attachment=img_file,
                        attachment_name=os.path.basename(image_path)
                    )
                    if attachment_result.get("addAttachmentResult", {}).get("success"):
                        print(f"📎 Image attached: {os.path.basename(image_path)}")
                    else:
                        print("⚠️ Failed to attach image:", attachment_result)

        else:
            print("❌ Failed to add feature:", result)
    except Exception as e:
        print("🌐 ArcGIS Push Error:", e)
