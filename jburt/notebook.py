"""
Utilities for working with Jupyter notebooks.
"""

import json

__all__ = ["read_ipynb", "code_from_nb", "code_from_file"]


def read_ipynb(path: str) -> dict:
    """
    Load cells from a Jupyter notebook into a dictionary.

    Args:
        path (str): Path to the Jupyter notebook.

    Returns:
        dict: Cells from the Jupyter notebook.
    """
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def prepend_header(src: str, i: int) -> str:
    """
    Prepend a header to a code cell.

    Args:
        src (str): Source code.
        i (int): Cell index.

    Returns:
        str: Source code with header prepended.
    """
    sep = f"# {'-' * (5 + len(str(i)))}"
    header = f"{sep}\n# Cell {i}\n{sep}\n"
    return "\n".join([header, src])


def validate_markdown(src: str) -> str:
    """
    Validate markdown source code.

    Args:
        src (str): Source code.

    Returns:
        str: Source code which shouldn't raise in a python script.
    """
    return "\n".join(
        [
            f"## {line.strip()}" if not line.strip().startswith("#") else line
            for line in src.split("\n")
        ]
    )


def fmt(cell: dict, cell_index: int = None) -> str:
    """
    Format a cell.

    Args:
        cell (dict): Cell from a Jupyter notebook.
        cell_index (int, optional): Cell index. Defaults to None.

    Returns:
        str: Formatted cell.
    """
    source = "".join(cell["source"])
    kind = cell["cell_type"].strip()

    if kind == "code":
        if cell_index is not None:
            return prepend_header(source, cell_index)
        return source
    elif kind == "markdown" or kind == "raw":
        return validate_markdown(source)
    else:
        raise ValueError("Unknown cell type: {0}".format(kind))


def edit(code: str, use_gpt_4: bool = False) -> str:
    """
    Reformat code using GPT-4.

    Args:
        code (str): Code to reformat.
        use_gpt_4 (bool, optional): Whether to use GPT-4. Defaults to False.

    Returns:
        str: Reformatted code.
    """
    if use_gpt_4:
        # code = get_response(code)
        raise NotImplementedError("GPT-4 not implemented yet")
    return code


def code_from_nb(notebook: dict, use_gpt_4=False) -> str:
    """
    Extract code from a Jupyter notebook.

    Args:
        notebook (dict): Jupyter notebook.
        use_gpt_4 (bool, optional): Whether to use GPT-4. Defaults to False.

    Returns:
        str: Code extracted from the Jupyter notebook.
    """
    cells = [fmt(cell, i) for i, cell in enumerate(notebook["cells"], start=1)]
    module = "\n\n".join(cells)
    if use_gpt_4:
        return edit(module)
    return module


def code_from_file(path: str, use_gpt_4=False) -> str:
    """
    Extract code from a Jupyter notebook file.

    Args:
        path (str): Path to the Jupyter notebook.
        use_gpt_4 (bool, optional): Whether to use GPT-4. Defaults to False.

    Returns:
        str: Code extracted from the Jupyter notebook.
    """
    nb = read_ipynb(path)
    return code_from_nb(nb, use_gpt_4)
