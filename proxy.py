
ALWAYS_EXCLUDE_NAMES = ('__class__', '__name__', '__doc__', '__new__' \
    , '__init__', '__getattribute__', '__subclasshook__', '__abstractmethods__' \
    , '__weakref__', '_abc_cache', '_abc_negative_cache' \
    , '_abc_negative_cache_version', '_abc_registry')
DEFAULT_EXCLUDE_NAMES = ('__getattr__', '__setattr__', '__delattr__')

from collections import Sequence
from abc import ABCMeta, abstractmethod, abstractproperty
from inspect import ismethod as isinstancemethod
from unique import uniques, uniquem


class Proxy(object):
  def __init__(self, *t, **d):
    pass


#TODO: handle variations such as static, class and property methods, plus 
#      variable properties and abstract things.
def defattr(cls, attr_name):
  attr = getattr(cls, attr_name)
  return lambda self,*t,**d: attr(self.__proxy__,*t,**d)


def proxy(obj, attr_names=None, exclude_attr_names=DEFAULT_EXCLUDE_NAMES \
    , proxy_name=None, mixins={}):
  """ 
  Create a Proxy class or a object proxy.
  
  Creates either a Proxy class or a object proxy depending on whether the first
  first argument is a type/class or an instance object.  All but the first 
  argument are optional.
  Note that proxying some attributes will create infinite recursion, which I am
  sure you're not interested in, so it's best to either use it without speicific
  attribute names or be selective with which attributes you really want to proxy.
  
  Parameters: 
    obj (object or type): the subject or type to proxy, 
    attr_names (Sequence): a Sequence attribute names you want proxied.
    exclude_attr_names (Sequence): a Sequence attribute names you do not want proxied.
    proxy_name (str): the name of the proxy class to generate.
    mixins (dict): non proxy methods or attributes to add in.
    subject (any): Not yet implemented.
  Returns: 
    object: the proxy object or type.
  """
  cls = obj if isinstance(obj, type) else obj.__class__
  if attr_names is None: attr_names = dir(obj)
  if mixins:
    exclude_attr_names = list(exclude_attr_names)
    for name in mixins.keys():
      if name not in exclude_attr_names:
        exclude_attr_names.append(name)
    exclude_attr_names = tuple(exclude_attr_names)
  attr_names = uniques(attr_names, exclude=uniques(ALWAYS_EXCLUDE_NAMES, exclude_attr_names))
  if proxy_name is None: proxy_name = '{:s}Proxy'.format(cls.__name__)
  if cls is obj:
    # class/type proxy
    attrs = dict((name, defattr(cls, name)) for name in attr_names \
        if name not in ALWAYS_EXCLUDE_NAMES \
        and name not in exclude_attr_names)
    attrs.update(mixins)
    attrs['__init__'] = lambda self, target: self.__setattr__('__proxy__', target)
    cls_proxy = type(proxy_name, (Proxy,), attrs)
    return cls_proxy
  
  # instance proxy
  attrs = dict((name, getattr(obj, name)) for name in attr_names \
      if name not in ALWAYS_EXCLUDE_NAMES \
      and name not in exclude_attr_names)
  attrs.update(mixins)
  obj_proxy = type(proxy_name, (Proxy,), attrs)
  return obj_proxy()


def proxy_sanity():
  a = {'a':1, 'b':2, 'c':3}
  b = proxy(a)
  assert b['a'] == a['a'] and 1 == a['a']
  b['a'] = 10
  assert b['a'] == a['a'] and 10 == a['a']


  C = proxy(dict)
  c = C(a)
  assert c['a'] == a['a'] and 10 == a['a']

  a['a'] = 1
  assert 1 == a['a']
  assert b['a'] == a['a']
  assert c['a'] == a['a']
