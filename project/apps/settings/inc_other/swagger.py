# Swagger doc settings

SWAGGER_SETTINGS = {
    'DOC_EXPANSION': 'none',
    'SECURITY_DEFINITIONS': {
        'Basic': {'type': 'basic'},
        'Bearer': {'type': 'apiKey', 'name': 'Authorization', 'in': 'header'},
    },
}
