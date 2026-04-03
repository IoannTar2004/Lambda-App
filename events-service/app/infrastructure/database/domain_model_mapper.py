from dataclasses import asdict

from bidict import bidict

from domain.models.execution_log import ExecutionLog
from domain.models.function_handler import FunctionHandler
from domain.models.project import Project
from domain.models.function import Function
from domain.models.project_revision import ProjectRevision
from domain.models.s3_function import S3Function
from infrastructure.database.models import *
from infrastructure.database.models.s3_function import S3FunctionModel

DOMAIN_MODEL_MAPPING = bidict({
    Function: FunctionModel,
    FunctionHandler: FunctionHandlerModel,
    Project: ProjectModel,
    S3Function: S3FunctionModel,
    ExecutionLog: ExecutionLogModel,
    ProjectRevision: ProjectRevisionModel
})

def model_to_domain(model, relations_to_extract: list[str] | None = None):
    domain_class = DOMAIN_MODEL_MAPPING.inverse[type(model)]
    data = {c.name: getattr(model, c.name) for c in model.__table__.columns}
    domain_obj = domain_class(**data)
    if relations_to_extract is not None:
        for relation in relations_to_extract:
            rel_value = getattr(model, relation)
            if rel_value is None:
                domain_obj.relations[relation] = {}
                continue
            if isinstance(rel_value, list):
                domain_obj.relations[relation] = [model_to_domain(m) for m in rel_value]
            else:
                domain_obj.relations[relation] = model_to_domain(rel_value)

    return domain_obj

def domain_to_model(domain):
    model_class = DOMAIN_MODEL_MAPPING[type(domain)]
    data = asdict(domain)
    data.pop("relations", None)
    print(f"Model class: {model_class.__name__}")
    print(f"Data keys: {data.keys()}")
    print(f"Model columns: {model_class.__table__.columns.keys()}")
    return model_class(**data)