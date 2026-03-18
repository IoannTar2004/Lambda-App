from dataclasses import asdict

from bidict import bidict

from domain.models.function_config import FunctionConfig
from domain.models.function_header import FunctionHeader
from infrastructure.database.models import FunctionHeaderModel, FunctionConfigModel

DOMAIN_MODEL_MAPPING = bidict({
       FunctionHeader: FunctionHeaderModel,
       FunctionConfig: FunctionConfigModel
})

def model_to_domain(model):
    domain_class = DOMAIN_MODEL_MAPPING.inverse[type(model)]
    data = {c.name: getattr(model, c.name) for c in model.__table__.columns}
    return domain_class(**data)

def domain_to_model(domain):
    model_class = DOMAIN_MODEL_MAPPING[type(domain)]
    data = asdict(domain)
    return model_class(**data)