from pydantic import RootModel
from typing import List

class FactsGapsOutput(RootModel[List[str]]):
    """
    A root model whose JSON value is a list of strings.
    """
    pass
