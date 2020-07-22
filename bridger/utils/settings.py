

def historical_models(historical_app_models):
    models = list()
    for app in historical_app_models:
        models.extend(list(map(lambda model: f"{app[0]}.{model}", app[1])))
    return models
