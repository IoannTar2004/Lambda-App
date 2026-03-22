from dataclasses import asdict

from bidict import bidict

from domain.models.function_handler import FunctionHandler
from domain.models.project import Project
from domain.models.function import Function
from domain.models.s3_function import S3Function
from infrastructure.database.models import *
from infrastructure.database.models.s3_function import S3FunctionModel

DOMAIN_MODEL_MAPPING = bidict({
    Function: FunctionModel,
    FunctionHandler: FunctionHandlerModel,
    Project: ProjectModel,
    S3Function: S3FunctionModel
})

def model_to_domain(model):
    domain_class = DOMAIN_MODEL_MAPPING.inverse[type(model)]
    data = {c.name: getattr(model, c.name) for c in model.__table__.columns}
    return domain_class(**data)

def domain_to_model(domain):
    model_class = DOMAIN_MODEL_MAPPING[type(domain)]
    data = asdict(domain)
    data.pop("relations", None)
    return model_class(**data)