import typing as t

from sqlalchemy.ext.declarative import as_declarative, declared_attr
from functools import wraps

class_registry: t.Dict = {}


@as_declarative(class_registry=class_registry)
class Base:
    id: t.Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


# Code got from https://github.com/tiangolo/fastapi/issues/2194 after doing some failure attempts from my side
# Combined with a init wrapper since nothing else from the site helped me solve the issue
def auto_init():  # sourcery no-metrics
    """Wraps the `__init__` method of a class to automatically set the common
    attributes.
    """

    def decorator(init):
        @wraps(init)
        def wrapper(self, *args, **kwargs):  # sourcery no-metrics
            """
            Custom initializer that allows nested children initialization.
            Only keys that are present as instance's class attributes are allowed.
            These could be, for example, any mapped columns or relationships.

            Code inspired from GitHub.
            Ref: https://github.com/tiangolo/fastapi/issues/2194
            """

            cls = self.__class__
            model_columns = self.__mapper__.columns
            relationships = self.__mapper__.relationships

            for key, val in kwargs.items():

                if not hasattr(cls, key):
                    raise TypeError(f"Invalid keyword argument: {key}")

                if key in model_columns:
                    setattr(self, key, val)
                    continue

                if key in relationships:
                    relation_cls = relationships[key].mapper.entity

                    if isinstance(val, list):
                        instances = [relation_cls(**elem) for elem in val]
                        setattr(self, key, instances)
                    elif isinstance(val, dict):
                        instance = relation_cls(**val)
                        setattr(self, key, instance)

            return init(self, *args, **kwargs)

        return wrapper

    return decorator
