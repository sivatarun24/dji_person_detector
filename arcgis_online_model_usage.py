from arcgis.gis import GIS
from arcgis.raster.analytics import predict_objects
from arcgis.raster import ImageryLayer

# Initialize GIS connection
gis = GIS("https://intern-hackathon.maps.arcgis.com", "your_username", "your_password")

# Hosted image service to run predictions on
image_service_url = "https://services.arcgis.com/your_org_id/arcgis/rest/services/your_image_layer/ImageServer"
img_layer = ImageryLayer(image_service_url, gis)

# Hosted deep learning package (.dlpk) on ArcGIS Online
model_item_id = "your_model_item_id"  # Replace with your actual item ID
model_item = gis.content.get(model_item_id)

# Run prediction
results = predict_objects(
    raster=img_layer,
    model=model_item,
    output_name="person_detection_output",
    compute_stats=True,
    context={"cellSize": 1}
)

# Output results (a new imagery layer or feature layer)
print("✅ Prediction completed. Output layer:")
print(results)
