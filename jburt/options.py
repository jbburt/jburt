from .objects import dotdict


def _pd_columns(module, n: int) -> None:
    module.set_option('display.max_columns', n)


def _pd_width(module, n: int) -> None:
    module.set_option('display.width', n)


def _pd_rows(module, n: int) -> None:
    module.set_option('display.max_rows', n)


def _pd_reset(module) -> None:
    module.reset_option('all')


pd = dotdict(
    {'columns': _pd_columns, 'width': _pd_width,
     'rows': _pd_rows, 'reset': _pd_reset}
)
