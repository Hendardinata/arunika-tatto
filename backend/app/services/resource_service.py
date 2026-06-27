from backend.app.repositories.domain_repositories import ArtistRepository, ServiceRepository, GalleryRepository

class ResourceService:
    def __init__(self):
        self.artist_repo = ArtistRepository()
        self.service_repo = ServiceRepository()
        self.gallery_repo = GalleryRepository()

    def get_artists(self, limit=0):
        return self.artist_repo.find_all(limit=limit)
        
    def get_services(self, limit=0):
        return self.service_repo.find_all(limit=limit)

    def get_gallery(self, limit=0):
        return self.gallery_repo.find_all(limit=limit)
