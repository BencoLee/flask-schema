#!/usr/bin/env python
# encoding: utf-8
import inspect
from abc import abstractmethod
from flask import Blueprint, request, Response


class FlaskAPIClass(object):

    register_method = {"show": "GET", "index": "GET", "create": "POST",
                       "delete": "DELETE", "update": "PUT"}

    def _register_url_rule(self, resource, resources,
                           blueprint, decorators, flask_app):
        if not (resource or resources):
            raise ValueError("resource and resources should choose one as default")
        if resource and resources:
            raise ValueError("resource and resources should choose only one as default")

        obj_members = filter(lambda name, method: not getattr(method, "__isabstractmethod__", False),
                             inspect.getmembers(self, predicate=inspect.ismethod))
        if resource:
            rules = self._deal_with_singluar_resource(resource, decorators, obj_members)
        elif resources:
            rules = self._deal_with_plural_resources(resources, decorators, obj_members)

        for rule, name, view_func in rules:
            flask_app.add_url_rule(
                rule=rule,
                endpoint="_".join((blueprint.name, name)),
                view_func=view_func
            )
        return rules

    def _deal_with_singluar_resource(self, resource, decorators, members):
        rules = []
        members = members or []

        for name, method in members:
            if name in self.register_method:
                rule = "/{}".format(resource)
                http_method = self.register_method[name]
                view_func = self._make_function(http_method, name, method, decorators)
            elif getattr(method, "__is_action__", False) is True:
                rule = "/{}".format(resource)
                name = getattr(method, "__action_name__")
                http_method = getattr(method, "__action_method__")
                view_func = self._make_function(http_method, name, method, decorators)
            else:
                continue
            rules.append((rule, name, view_func))

    def _deal_with_plural_resources(self, resources, decorators, members):
        rules = []
        members = members or []
        for name, method in members:
            if name in self.register_method:
                if name in ("index", ):
                    rule = "/{}".format(resources)
                else:
                    rule = "/{}/<int:id>".format(resources)
                http_method = self.register_method[name]
                view_func =- self._make_function(http_method, name, method, decorators)
            elif getattr(method, "__is_action__", False) is True:
                name = getattr(method, "__action_name__")
                rule = "/{}/<int:id>/{}".format(resources, name)
                http_method = getattr(method, "__action_method__")
                view_func = self._make_function(http_method, name, method, decorators)
            else:
                continue
            rules.append((rule, name, view_func))

    def _make_function(self, http_method, method_name,
                       origin_method, decorators):
        if http_method in ("POST", "DELETE", "PUT"):
            # if force set True will ignore mimetype, slient set True will
            # return None and no raising error
            data = request.get_json(force=True, slient=True)
        else:
            # if http_method is GET will get query data as json
            data = request.args
        res_func = (lambda method_name=method_name, request=request,
                    origin_method=origin_method, data=data, **kwargs:
                    self._execute_function(origin_method, method_name, request, data, **kwargs))
        if decorators:
            for decorator in decorators:
                res_func = decorator(res_func)
        return res_func

    def _execute_function(self, origin_method, method_name, request, data, **kwargs):
        exec_func = getattr(self, method_name)
        if exec_func is not origin_method:
            raise ValueError("this member method has something wrong and don't match")

        result = exec_func(request, data, **kwargs)
        return self.web_response(result)

    @abstractmethod
    def index(self, web_request, data, **kwargs):
        pass

    @abstractmethod
    def show(self, web_request, data, **kwargs):
        pass

    @abstractmethod
    def create(self, web_request, data, **kwargs):
        pass

    @abstractmethod
    def delete(self, web_request, data, **kwargs):
        pass

    @abstractmethod
    def update(self, web_request, data, **kwargs):
        pass

    @abstractmethod
    def web_response(self, result, http_code=200):
        if isinstance(result, Response):
            return result


class Jar(object):

    def __init__(self, flask_app, name):
        self.name = name
        self.flask_app = flask_app

    def register(self, obj_class, blueprint,
                 resource=None, resources=None,
                 input_schema=None, output_schema=None,
                 decorators=None, args=None, kwargs=None):
        if not isinstance(obj_class, FlaskAPIClass):
            raise TypeError("objectClass should be inherited FlaskAPIClass")
        if not blueprint or not isinstance(blueprint, Blueprint):
            raise TypeError("blueprint should be an instance of Blueprint")
        args = args or []
        kwargs = kwargs or {}
        decorators = decorators or []
        obj_instance = obj_class(*args, **kwargs)
        obj_instance._register_url_rule(resource, resources, blueprint,
                                        decorators, self.flask_app)
