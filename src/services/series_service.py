"""Servicio de Series."""
from src.services.base_service import BaseService


class SeriesService(BaseService):
    def __init__(self, series_repository):
        super().__init__(series_repository)
