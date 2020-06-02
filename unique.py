from collections import Sequence, Mapping

def uniques(*seqs, **kwargs):
  """ 
  Extracts all unique items for a series of sequences.
  
  All non-keyword arguments will be treat as sequences to extract unique values from.
  You may also use the keyword argument 'exclude' as a sequence of values to filter out.
  
  Parameters: 
    *seqs (Sequences): a series of value sequences 
    exclude (Sequence): a Sequence of values to filter out 
  Returns: 
    Sequence: the unique filtered values as whatever the first argument type was.
  """
  excludes = kwargs['exclude'] if 'exclude' in kwargs else ()
  if not all(isinstance(names, Sequence) for names in seqs):
    raise TypeError('invalid arguments, expected Sequences but found: ({:s})' \
        .format(', '.join(type(arg for arg in seqs).__name__)))
  if not isinstance(excludes, Sequence):
    raise TypeError('invalid exclude, expected a Sequence but found: ({:s})' \
        .format(type(excludes).__name__))
  kwargnames = tuple(name for name in kwargs.keys() if name != 'exclude')
  if kwargnames:
    raise ValueError('invalid keyword arguments: ' + ', '.join(kwargnames))
  return type(seqs[0])(reduce(lambda b,s: reduce(lambda a,v: a \
      if v in a or v in excludes else a+(v,), s, b), seqs, ()))

def uniquem(*maps, **kwargs):
  """ 
  Extracts all unique items for a series of mappings.
  
  All non-keyword arguments will be treat as mappings to extract unique items from.
  You may also use the keyword arguments 'exclude_keys' or 'exclude_values' as a 
  sequence of values to filter out.
  
  Parameters: 
    *maps (Mappings): a series of value sequences 
    exclude_keys (Sequence): a Sequence of keys to filter out 
    exclude_values (Sequence): a Sequence of values to filter out 
  Returns: 
    Mapping: the unique filtered items as whatever the first argument type was.
  """
  if not all(isinstance(d, Mapping) for d in maps):
    raise TypeError('invalid arguments, expected Mappings but found: ({:s})' \
        .format(', '.join(type(arg for arg in maps).__name__)))
  exkeys = kwargs['exclude_keys'] if 'exclude_keys' in kwargs else ()
  if not isinstance(exkeys, Sequence):
    raise TypeError('invalid exclude_keys, expected a Sequence but found: ({:s})' \
        .format(type(exkeys).__name__))
  exvalues = kwargs['exclude_values'] if 'exclude_values' in kwargs else ()
  if not isinstance(exvalues, Sequence):
    raise TypeError('invalid exclude_values, expected a Sequence but found: ({:s})' \
        .format(type(exvalues).__name__))
  kwargnames = tuple(name for name in kwargs.keys() \
      if name not in ('exclude_keys', 'exclude_values'))
  if kwargnames:
    raise ValueError('invalid keyword arguments: ' + ', '.join(kwargnames))
  result = {}
  for d in maps:
    for (k,v) in d.items():
      if k not in result and k not in exkeys and v not in exvalues:
        result[k] = v
  return result
