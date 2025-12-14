from locust import HttpUser, task, between

class MapServerUser(HttpUser):
    # Czas oczekiwania między zapytaniami (symulacja myślenia użytkownika)
    wait_time = between(0.1, 0.5)

    @task
    def get_map(self):
        # Zapytanie WMS GetMap (skopiowane z Twojego przykładu)
        wms_params = (
            "/ogc?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap"
            "&BBOX=3038576.234106336255%2C5032438.927781008184%2C3052011.334363552276%2C5043857.993520818651"
            "&CRS=EPSG:3035&WIDTH=1484&HEIGHT=1746"
            "&LAYERS=URBAN_ATLAS_COG&STYLES=&FORMAT=image/png"
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
