import sys
import textwrap
from typing import Any, Dict

from django.core.management import color_style

try:
    # PEP8-compliant pprint implementation
    from pprintpp import pformat
except ImportError:
    from pprint import pformat

try:
    from pygments import highlight, lexers, formatters
    HAS_PYGMENTS = True
except ImportError:
    HAS_PYGMENTS = False

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


__all__ = [
    'pformat_highlighted',
    'pprint_highlighted',
    'pformat_yaml',
    'pprint_yaml',
    'pformat_event',
    'pprint_event',
]


if HAS_PYGMENTS:
    term_formatter = formatters.get_formatter_by_name('terminal256', style='monokai')

    def syntax_highlight(source: str, lang: str = 'python') -> str:
        lexer = lexers.get_lexer_by_name(lang)
        return highlight(source, lexer, term_formatter)

else:
    def syntax_highlight(source: str, lang: str = 'python') -> str:
        return source


style = color_style()


def pformat_highlighted(o) -> str:
    """Return the pretty-printed repr of an object, with highlighting if available
    """
    return syntax_highlight(pformat(o))


def pprint_highlighted(o, stream=sys.stderr) -> None:
    """Pretty-print an object to stdout, with highlighting if available
    """
    print(pformat_highlighted(o), file=stream)


def pformat_yaml(o) -> str:
    """Return the YAML representation of an object, with highlighting if available
    """
    if not HAS_YAML:
        raise RuntimeError(
            'PyYAML is not available to format YAML. '
            'To use YAML formatting, install the "highlighting" extra: '
            'pip install slack-channeler[highlighting]')

    return syntax_highlight(yaml.dump(o, default_flow_style=False), 'yaml')


def pprint_yaml(o, stream=sys.stderr) -> None:
    """Print YAML representation of an object, with highlighting if available
    """
    print(pformat_yaml(o), file=stream)


def pformat_event(event_type: str, data: Dict[str, Any]) -> str:
    """Return pretty repr of an event and its data

    The event type will be printed at the top in red. The data will be printed
    as YAML, if PyYAML installed; otherwise, it will be pretty-printed Python —
    using pprintpp if it's installed, and falling back on vanilla pprint. The
    data will be syntax-highlighted, if pygments installed.
    """
    header = style.SUCCESS(event_type)

    if HAS_YAML:
        body = pformat_yaml(data)
        body = textwrap.indent(body, '  ')
    else:
        body = pformat_highlighted(data)

    return header + '\n' + body


def pprint_event(event_type: str, data: Dict[str, Any], stream=sys.stderr) -> None:
    """Print a pretty representation of an event

    See pformat_event() for details.
    """
    print(pformat_event(event_type, data), file=stream)
