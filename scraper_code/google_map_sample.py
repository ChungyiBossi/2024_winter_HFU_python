
import os
from pprint import pprint
import requests
import json
import geocoder


def get_place_detail_fields():
    # https://developers.google.com/maps/documentation/places/web-service/data-fields?hl=zh-tw
    return [
        'places.location',
        'places.displayName',
        'places.formattedAddress',
        'places.reviews',
        'places.rating',
        'places.allowsDogs'
    ]


def search_place_by_name(api_key, text_query, fields=get_place_detail_fields()):
    URL = "https://places.googleapis.com/v1/places:searchText"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": ",".join(fields)  # 只获取名称、地址和价格等级
    }

    payload = {
        "textQuery": text_query  # 搜索 "悉尼的素食辣味餐厅"
    }

    response = requests.post(URL, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        results = response.json().get("places", [])
        if results:
            return results
        else:
            print("❌ 没有找到符合条件的地点。")
    else:
        print(f"❌ 请求失败，状态码: {response.status_code}, 错误信息: {response.text}")

    return list()


def search_nearby_places(api_key, lat, lon, fields=get_place_detail_fields(), radius=1000, place_type=['restaurant'], max_count=10):
    URL = "https://places.googleapis.com/v1/places:searchNearby"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": ",".join(fields)
    }

    payload = {
        # Ref Place Table: https://developers.google.com/maps/documentation/places/web-service/place-types?hl=zh-tw#table-a
        "includedTypes": place_type,
        "maxResultCount": max_count,  # 返回最多 10 个结果
        "locationRestriction": {
            "circle": {
                "center": {"latitude": lat, "longitude": lon},  # 目标位置
                "radius": radius
            }
        }
    }

    response = requests.post(URL, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        results = response.json()
        return results.get("places", [])
    else:
        print(f"❌ 请求失败，状态码: {response.status_code}, 错误信息: {response.text}")
        return list()


# Not sure if nearby_search could completely replace this api
# def search_place_detail(api_key, place_id):

#     URL = f"https://places.googleapis.com/v1/places/{place_id}"

#     headers = {
#         "Content-Type": "application/json",
#         "X-Goog-Api-Key": API_KEY,
#         "X-Goog-FieldMask": "id,displayName, reviews"  # 只获取 ID 和名称
#     }

#     response = requests.get(URL, headers=headers)

#     if response.status_code == 200:
#         result = response.json()
#         return result
#     else:
#         print(f"❌ 请求失败，状态码: {response.status_code}, 错误信息: {response.text}")
#         return list()


if __name__ == "__main__":
    API_KEY = os.getenv("GOOGLE_MAP_API_KEY")
    # Find Place
    # LAT, LON = geocoder.ip('me').latlng

    r = search_place_by_name(API_KEY, '勤美誠品')
    print("First One: ", r[0])

    location = r[0]['location']
    LAT, LON = location['latitude'], location['longitude']
    places = search_nearby_places(API_KEY, LAT, LON, max_count=20, place_type=[
                                  'dog_cafe', 'cat_cafe', 'restaurant'])  # place type 協助篩選

    for place in places:
        is_allow_dogs = place.get('allowsDogs', False)
        if is_allow_dogs:
            print(f"📍 地点名称: {place.get('displayName', {}).get('text', '未知')}")
            pprint(place)
