import math
from geopy.distance import geodesic

def map_to_coordinates(boxes, metadata):
    coords = []

    # Extract DJI-style fields
    lat = metadata.get('latitude')
    lon = metadata.get('longitude')
    height = metadata.get('altitude')  # in meters
    yaw = metadata.get('yaw')          # in degrees
    pitch = metadata.get('pitch')      # camera pitch (negative looking down)
    fov = metadata.get('fov', 82.6)    # horizontal FOV in degrees
    resolution = metadata.get('resolution', [720, 960])  # [height, width]

    frame_height, frame_width = resolution
    frame_center_x = frame_width // 2

    for (x1, y1, x2, y2) in boxes:
        person_x = (x1 + x2) // 2
        dx_pixels = person_x - frame_center_x

        # Horizontal angular offset of detected person
        pixel_angle = (dx_pixels / frame_width) * fov

        # Total camera angle toward the object
        total_angle = pitch + pixel_angle  # pitch usually negative

        # Calculate ground distance from drone to object (basic triangulation)
        ground_dist = height * math.tan(math.radians(-total_angle))

        # Project location forward from drone GPS using drone yaw
        new_coord = calculate_offset((lat, lon), yaw, ground_dist)
        coords.append(new_coord)

    return coords

def calculate_offset(start_coord, bearing_deg, distance_m):
    """
    Given a starting GPS coord (lat, lon), bearing in degrees,
    and distance in meters, return new (lat, lon).
    """
    return geodesic(meters=distance_m).destination(start_coord, bearing_deg)
