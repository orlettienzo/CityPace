import requests
import polyline

def get_street_polyline_latlng(name, postal_code) -> str:
    """Retourne la liste des coordonnées de la polyline de la rue en utilisant geopy."""
    url = f"https://nominatim.openstreetmap.org/search?q={name}, {postal_code}, Belgium&format=json"
    try:
        result = requests.get(url=url, timeout=10)
        print(f"{result=}")
        result_json = result.json()
        # print(f"{result_json=}")
        if len(result_json) > 0:
            latitude = result_json[0]['lat']
            longitude = result_json[0]['lon']
            polyline_url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}"
            print(f"{polyline_url=}")
            polyline_result = requests.get(url=polyline_url, timeout=10)
            polyline_data = polyline_result.json()
            if 'osm_way' in polyline_data:
                encoded_polyline = polyline_data['osm_way']
                decoded_polyline = polyline.decode(encoded_polyline)
                return decoded_polyline
            else:
                print("Error: Polyline data not found")
                return ""
        else:
            print("Error: No result found")
            return ""
    except Exception as e:
        print(f"Error: {e}")
        return ""

coordinates = get_street_polyline_latlng("Eikenlei", "2280")
print(coordinates)


# {'place_id': 123124363, 'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright', 'osm_type': 'way', 'osm_id': 197924435, 'lat': '51.1888767', 'lon': '4.7184143', 'class': 'highway', 'type': 'unclassified', 'place_rank': 26, 'importance': 0.10000999999999993, 'addresstype': 'road', 'name': 'Eikenlei', 'display_name': 'Eikenlei, Grobbendonk, Turnhout, Antwerpen, Vlaanderen, 2280, België / Belgique / Belgien', 'boundingbox': ['51.1882462', '51.1903063', '4.7109644', '4.7281326']}, 
# {'place_id': 124023916, 'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright', 'osm_type': 'way', 'osm_id': 588795298, 'lat': '51.2629827', 'lon': '4.5576159', 'class': 'highway', 'type': 'residential', 'place_rank': 26, 'importance': 0.10000999999999993, 'addresstype': 'road', 'name': 'Eikenlei', 'display_name': "Eikenlei, 's-Gravenwezel, Schilde, Antwerpen, Vlaanderen, 2970, België / Belgique / Belgien", 'boundingbox': ['51.2629636', '51.2629827', '4.5575327', '4.5576159']}, 
# {'place_id': 123154395, 'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright', 'osm_type': 'way', 'osm_id': 23088769, 'lat': '51.3041785', 'lon': '4.5678093', 'class': 'highway', 'type': 'secondary', 'place_rank': 26, 'importance': 0.10000999999999993, 'addresstype': 'road', 'name': 'Eikenlei', 'display_name': "Eikenlei, Sint-Job-in-'t-Goor, Brecht, Antwerpen, Vlaanderen, 2960, België / Belgique / Belgien", 'boundingbox': ['51.3040988', '51.3042151', '4.5676351', '4.5679108']}, 
# {'place_id': 123610092, 'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright', 'osm_type': 'way', 'osm_id': 1084205751, 'lat': '51.2972673', 'lon': '4.5533332', 'class': 'highway', 'type': 'secondary', 'place_rank': 26, 'importance': 0.10000999999999993, 'addresstype': 'road', 'name': 'Eikenlei', 'display_name': "Eikenlei, Sint-Job-in-'t-Goor Zone 1 - Kloosterveld, Sint-Job-in-'t-Goor, Brecht, Antwerpen, Vlaanderen, 2960, België / Belgique / Belgien", 'boundingbox': ['51.2969955', '51.2981090', '4.5528012', '4.5549195']}