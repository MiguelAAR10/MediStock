from services.api_client import api_client


class MLClient:
    def get_forecasting_data(self, fecha_inicio=None, fecha_fin=None):
        return api_client.get_ventas_diarias(fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)

    def get_clustering_data(self):
        return api_client.get_clientes_analytics()

    def get_segmentos(self):
        return api_client.get_segmentos()


ml_client = MLClient()
