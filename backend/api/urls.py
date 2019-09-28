from .views import (
    PingView,
    GetTextView,
    GetOfferView,
)


def set_urls(api, config):
    GetOfferView.CONFIG = config
    GetTextView.CONFIG = config
    api.add_resource(GetTextView, '/api/text/')
    api.add_resource(GetOfferView, '/api/offer/')
    api.add_resource(PingView, '/ping/')
