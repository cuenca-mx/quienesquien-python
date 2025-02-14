class QuienEsQuienError(Exception):
    """
    Lanzado cuando se produce un error al usar la API de QuienEsQuien.
    """


class InvalidSearchCriteriaError(QuienEsQuienError):
    """
    Lanzado cuando no se proporcionan los parámetros de búsqueda necesarios.
    """


class PersonNotFoundError(QuienEsQuienError):
    """
    Lanzado cuando no se encuentran coincidencias con los parámetros de
    búsqueda especificados.
    """


class InvalidTokenError(QuienEsQuienError):
    """
    Lanzado cuando el token utilizado para realizar la búsqueda es inválido.
    """


class InvalidPlanError(QuienEsQuienError):
    """
    Lanzado cuando el servicio contratado ya no se encuentra vigente.
    """


class InsufficientBalanceError(QuienEsQuienError):
    """
    Lanzado cuando no se cuenta con saldo suficiente (QTokens) para
    realizar la búsqueda.
    """
