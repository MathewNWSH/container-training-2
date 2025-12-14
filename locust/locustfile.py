import random

from locust import HttpUser, task, between

class MapServerUser(HttpUser):
    # Czas oczekiwania między zapytaniami (symulacja myślenia użytkownika)
    wait_time = between(0.1, 0.5)

    BASE_BBOX = {
        "minx": 3038990.1236336227,
        "miny": 5033242.812142192,
        "maxx": 3042995.7642743285,
        "maxy": 5037487.047643513,
    }

    # Rozmiar losowego podglądu mapy (w jednostkach BBOX)
    SAMPLE_WIDTH = 500
    SAMPLE_HEIGHT = 500

    @task
    def get_map(self):
        # Losuj pod-bbox mieszczący się w zgłoszonym zakresie
        x_range = self.BASE_BBOX["maxx"] - self.BASE_BBOX["minx"] - self.SAMPLE_WIDTH
        y_range = self.BASE_BBOX["maxy"] - self.BASE_BBOX["miny"] - self.SAMPLE_HEIGHT

        minx = self.BASE_BBOX["minx"] + random.random() * x_range
        miny = self.BASE_BBOX["miny"] + random.random() * y_range
        maxx = minx + self.SAMPLE_WIDTH
        maxy = miny + self.SAMPLE_HEIGHT

        wms_params = (
            "/mapserver?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap"
            f"&BBOX={minx:.6f}%2C{miny:.6f}%2C{maxx:.6f}%2C{maxy:.6f}"
            "&CRS=EPSG:3035&WIDTH=925&HEIGHT=873"
            "&LAYERS=Krakow_UA_2021_Vector&STYLES=&FORMAT=image/png"
            "&DPI=192&MAP_RESOLUTION=192&FORMAT_OPTIONS=dpi:192&TRANSPARENT=TRUE"
        )
        
        with self.client.get(wms_params, catch_response=True) as response:
            if response.status_code == 200:
                # Opcjonalnie: sprawdź czy to faktycznie obrazek
                if response.headers.get("Content-Type") == "image/png":
                    response.success()
                else:
                    response.failure(f"Wrong content-type: {response.headers.get('Content-Type')}")
            else:
                response.failure(f"Status code: {response.status_code}")
