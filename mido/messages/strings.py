from .specs import SPEC_BY_TYPE, make_msgdict


def msg2str(msg, include_time=True):
    type_ = msg['type']
    spec = SPEC_BY_TYPE[type_]

    words = [type_]

    for name in spec['value_names']:
        words.append('{}={}'.format(name, msg[name]))

    if include_time:
        words.append('time={}'.format(msg['time']))
    
    return str.join(' ', words)


def _parse_time(value):
    # Convert to int if possible.
    try:
        return int(value)
    except ValueError:
        pass

    try:
        return float(value)
    except ValueError:
        pass

    raise ValueError('invalid time {!r}'.format(value))


def str2msg(text):
    type_, *args = text.split()

    msg = {}

    for arg in args:
        name, value = arg.split('=', 1)
        if name == 'time':
            value = _parse_time(value)
        else:
            value = int(value)

        msg[name] = value

    # Todo: hmm, this needs to be rethought.
    # Where should the type and value checking happen?
    return make_msgdict(type_, **msg)
