import uuid

from functional.settings import test_settings


def get_es_data(test_for: str):
    match test_for:
        case 'search':
            es_data = [{
                "id": str(uuid.uuid4()),
                "imdb_rating": 6.1,
                "genres": [{"id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff", "name": "Action"},
                           {"id": "6c162475-c7ed-4461-9184-001ef3d9f26e", "name": "Sci-Fi"}],
                "title": "Kinect Star Wars",
                "description": "",
                "directors_names": ["Ali Donovan", "Jorg Neumann"],
                "actors_names": ["Jean Gilpin", "Jennifer Hale", "Nolan North", "Tom Kane"],
                "writers_names": [],
                "directors": [{"id": "1b4d95d8-b093-49f3-b67a-1f4fd7589180", "name": "Ali Donovan"},
                              {"id": "9b475aa1-8a72-4af1-ac01-3e5871298c74", "name": "Jorg Neumann"}],
                "actors": [{"id": "00395304-dd52-4c7b-be0d-c2cd7a495684", "name": "Jennifer Hale"},
                           {"id": "35ded0cd-785e-4f61-80f1-08538b34f660", "name": "Nolan North"},
                           {"id": "5237aac5-f652-4aa5-9061-55bb007cd7be", "name": "Tom Kane"},
                           {"id": "d9f1ecbd-98b7-4aa4-a82e-da87cdb12b8e", "name": "Jean Gilpin"}],
                "writers": []
            } for _ in range(50)]
        case 'search_valid':
            es_data = [{
                "id": "3d8d9bf5-13ed-4353-88ba-4ccc5d2c07ff",
                "imdb_rating": 'qwerty',
                "genres": [{"id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff", "name": "Action"},
                           {"id": "6c162475-c7ed-4461-9184-001ef3d9f26e", "name": "Sci-Fi"}],
                "title": "Kinect Star Wars",
                "description": None,
                "directors_names": ["Ali Donovan", "Jorg Neumann"],
                "actors_names": ["Jean Gilpin", "Jennifer Hale", "Nolan North", "Tom Kane"],
                "writers_names": [],
                "directors": [{"id": "1b4d95d8-b093-49f3-b67a-1f4fd7589180", "name": "Ali Donovan"},
                              {"id": "9b475aa1-8a72-4af1-ac01-3e5871298c74", "name": "Jorg Neumann"}],
                "actors": [{"id": "00395304-dd52-4c7b-be0d-c2cd7a495684", "name": "Jennifer Hale"},
                           {"id": "35ded0cd-785e-4f61-80f1-08538b34f660", "name": "Nolan North"},
                           {"id": "5237aac5-f652-4aa5-9061-55bb007cd7be", "name": "Tom Kane"},
                           {"id": "d9f1ecbd-98b7-4aa4-a82e-da87cdb12b8e", "name": "Jean Gilpin"}],
                "writers": []
            }]
        case "film_by_id":
            es_data = [{
                "id": '5ghd9bf5-0d90-4353-88ba-4ccc5d2c07ff',
                "imdb_rating": 6.1,
                "genres": [{"id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff", "name": "Action"},
                           {"id": "6c162475-c7ed-4461-9184-001ef3d9f26e", "name": "Sci-Fi"}],
                "title": "Kinect Star Wars",
                "description": "",
                "directors_names": ["Ali Donovan", "Jorg Neumann"],
                "actors_names": ["Jean Gilpin", "Jennifer Hale", "Nolan North", "Tom Kane"],
                "writers_names": [],
                "directors": [{"id": "1b4d95d8-b093-49f3-b67a-1f4fd7589180", "name": "Ali Donovan"},
                              {"id": "9b475aa1-8a72-4af1-ac01-3e5871298c74", "name": "Jorg Neumann"}],
                "actors": [{"id": "00395304-dd52-4c7b-be0d-c2cd7a495684", "name": "Jennifer Hale"},
                           {"id": "35ded0cd-785e-4f61-80f1-08538b34f660", "name": "Nolan North"},
                           {"id": "5237aac5-f652-4aa5-9061-55bb007cd7be", "name": "Tom Kane"},
                           {"id": "d9f1ecbd-98b7-4aa4-a82e-da87cdb12b8e", "name": "Jean Gilpin"}],
                "writers": []
            }]
        case 'list_genres':
            es_data = [{
                "id": str(uuid.uuid4()),
                "name": "Action",
                "description": None,
                "films": [
                    {
                        "id": "00af52ec-9345-4d66-adbe-50eb917f463a",
                        "title": "Star Slammer"
                    },
                ]
            } for _ in range(10)]
        case 'genres_by_id':
            es_data = [{
                "id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff",
                "name": "Action",
                "description": None,
                "films": [
                    {
                        "id": "00af52ec-9345-4d66-adbe-50eb917f463a",
                        "title": "Star Slammer"
                    },
                ]
            }]

        case 'genres_valid':
            es_data = [{
                "id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff",
                "name": 1,
                "description": None,
                "films": [
                    {
                        "id": "00af52ec-9345-4d66-adbe-50eb917f463a",
                        "title": "Star Slammer"
                    },
                ]
            }]

        case 'list_persons':
            es_data = [{
                "id": str(uuid.uuid4()),
                "name": "John Snow",
                "films": [
                    {
                        "id": "00af52ec-9345-4d66-adbe-50eb917f463a",
                        "roles": ["actor"],
                        "imdb_rating": 7.8
                    },
                ]
            } for _ in range(10)]

        case 'person_by_id':
            es_data = [{
                "id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff",
                "name": "John Snow",
                "films": [
                    {
                        "id": "00af52ec-9345-4d66-adbe-50eb917f463a",
                        "roles": ["actor"],
                        "imdb_rating": 7.8
                    },
                ]
            }]

        case 'persons_valid':
            es_data = [{
                "id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff",
                "name": 1,
                "films": [
                    {
                        "id": "00af52ec-9345-4d66-adbe-50eb917f463a",
                        "roles": ["actor"],
                        "imdb_rating": 7.8
                    },
                ]
            }]

    return es_data
