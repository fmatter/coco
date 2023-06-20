from clld.web.maps import Map, Layer, GeoJsonSelectedLanguages
from clld.web.util import helpers
from clld.web.adapters.geojson import GeoJson, get_lonlat, get_feature
from pyramid.renderers import render as pyramid_render
from clld import interfaces


class GeoJsonCognates(GeoJson):
    def feature_iterator(self, ctx, req):
        return self.obj

    def get_features(self, ctx, req):
        map_marker = req.registry.getUtility(interfaces.IMapMarker)

        for feature in self.feature_iterator(ctx, req):
            language = feature.language
            lonlat = get_lonlat(language)
            if lonlat:
                properties = self.feature_properties(ctx, req, feature) or {}
                properties.setdefault("icon", map_marker(feature, req))
                properties.setdefault("language", language)
                properties.setdefault("label", feature.name)
                yield get_feature(language, lonlat=lonlat, **properties)


class CognatesetMap(Map):
    def get_layers(self):
        if self.ctx.reflexes:
            lgs = []
            for reflex in self.ctx.reflexes:
                lgs.append(reflex.counterpart)
            layer = Layer(
                id_="reflexes",
                name="reflexes",
                data=GeoJsonCognates(lgs).render(self.ctx, self.req, dump=False),
            )
            yield layer

    def get_default_options(self):
        return {
            "show_labels": True,
            "resize_direction": "s",
            "info_query": {"parameter": self.ctx.pk},
            "hash": True,
        }
