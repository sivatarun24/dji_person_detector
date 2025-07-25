# arcgis_client.py
from arcgis.gis import GIS
from arcgis.features import FeatureLayer
import os

class ArcGISClient:
    def __init__(self, username, password, org_url, layer_url):
        self.gis = GIS(org_url, username, password)
        self.layer = FeatureLayer(layer_url)

    def push_location(self, lat, lon, image_path=None, name="Person", status="Detected"):
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
            result = self.layer.edit_features(adds=[new_feature])
            if result.get("addResults") and result["addResults"][0]["success"]:
                object_id = result["addResults"][0]["objectId"]
                print(f"✅ Feature added: ({lat}, {lon}) with objectId={object_id}")

                # Attach image if path provided
                if image_path and os.path.exists(image_path):
                    with open(image_path, 'rb') as img_file:
                        attach_result = self.layer.attachments.add(
                            object_id=object_id,
                            attachment=img_file,
                            attachment_name=os.path.basename(image_path)
                        )
                        if attach_result.get("addAttachmentResult", {}).get("success"):
                            print(f"📎 Image attached: {os.path.basename(image_path)}")
                        else:
                            print("⚠️ Failed to attach image:", attach_result)

            else:
                print("❌ Failed to add feature:", result)

        except Exception as e:
            print("🌐 ArcGIS Push Error:", e)

    def get_all_locations(self):
        try:
            results = self.layer.query(
                where="1=1",
                out_fields="*",
                return_geometry=True,
                out_sr=4326,
                result_record_count=-1
            ).features

            print(f"📦 Total features: {len(results)}")
            for f in results:
                attrs = f.attributes
                geom = f.geometry
                print(f"OBJECTID: {attrs['OBJECTID']}, Name: {attrs.get('Name')}, X: {geom['x']}, Y: {geom['y']}")
        except Exception as e:
            print("🛑 Query failed:", e)
