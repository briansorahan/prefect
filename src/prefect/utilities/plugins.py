import prefect
from typing import Callable

from box import Box
import importlib

REGISTRY = Box(api=Box(), models=Box(), plugins=Box())
API = REGISTRY.api
MODELS = REGISTRY.models
PLUGINS = REGISTRY.plugins


def import_on_start_modules():
    """
    Imports on-start modules from config
    """
    for module in prefect.config.import_on_start:
        importlib.import_module(module)


def _register(name: str, registry: dict):
    """
    A decorator for registering an object to a registry.
    """

    def _register(obj):
        nonlocal registry
        keys = name.split(".")
        for key in keys[:-1]:
            registry = registry.setdefault(key, Box())
        registry[keys[-1]] = obj
        return obj

    return _register


def register_api(name: str) -> Callable:
    """
    Register an API function.

    Args:
        - name (str): the dot-delimited qualified name for the API function

    @register_api("fns.my_fn")
    def f(x):
        return x + 1

    assert API.fns.my_fn(100) == 101

    """
    return _register(name, registry=API)


def register_model(name: str) -> Callable:
    return _register(name, registry=MODELS)


def register_plugin(name: str) -> Callable:
    return _register(name, registry=PLUGINS)