from .models import FeatureToggle

def global_feature_toggles(request):
    toggle, created = FeatureToggle.objects.get_or_create(id=1)
    return {'feature_toggles': toggle}
