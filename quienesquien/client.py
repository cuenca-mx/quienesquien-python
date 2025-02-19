import datetime as dt
from dataclasses import dataclass, field
from typing import Mapping

import httpx

from .enums import Gender, SearchList, SearchType
from .exc import (
    InsufficientBalanceError,
    InvalidPlanError,
    InvalidSearchCriteriaError,
    InvalidTokenError,
    PersonNotFoundError,
    QuienEsQuienError,
)
from .person import Person

NOT_FOUND_ERROR_RESPONSE = 'No se han encontrado coincidencias'
INVALID_TOKEN_ERROR_RESPONSE = (
    'El token proporcionado para realizar esta acción es inválido'
)
INVALID_PLAN_ERROR_RESPONSE = (
    'Tu plan de consultas ha expirado, '
    'por favor actualiza tu plan para continuar usando la API'
)
INSUFFICIENT_BALANCE_ERROR_RESPONSE = (
    'No se puede realizar la búsqueda, saldo insuficiente'
)


@dataclass
class Client:
    base_url = 'https://app.q-detect.com'
    username: str
    client_id: str
    secret_key: str
    _auth_token: str | None = None
    _client: httpx.AsyncClient = field(
        default_factory=httpx.AsyncClient, init=False
    )

    def _invalidate_auth_token(self) -> None:
        """Clear the stored authentication token."""
        self._auth_token = None

    async def _make_request(
        self,
        method: str,
        url: str,
        *,
        headers: Mapping[str, str] | None = None,
        params: Mapping[str, str | int | None] | None = None,
    ) -> httpx.Response:
        """Make an HTTP request using an async client."""
        response = await self._client.request(
            method, url, headers=headers, params=params
        )
        response.raise_for_status()
        return response

    async def _fetch_auth_token(self) -> str:
        """Retrieve authentication token from the API."""
        if self._auth_token is not None:
            return self._auth_token

        auth_url = f'{self.base_url}/api/token'
        params = {'client_id': self.client_id}
        headers = {
            'Authorization': f'Bearer {self.secret_key}',
            'Accept-Encoding': 'identity',
        }

        response = await self._make_request(
            'GET', auth_url, headers=headers, params=params
        )
        self._auth_token = response.text
        return self._auth_token

    async def search(
        self,
        full_name: str | None = None,
        match_score: int = 60,  # Default 60, applied even if no value provided
        rfc: str | None = None,
        curp: str | None = None,
        gender: Gender | None = None,
        birthday: dt.date | None = None,
        search_type: SearchType | None = None,
        search_list: tuple[SearchList, ...] | None = None,
    ) -> list[Person]:
        """Perform a search request and return the results.

        Args:
            full_name (str): Full name of the person.
            match_score (int): Minimum match percentage (default: 60).
            rfc (str): Mexican RFC.
            curp (str): Mexican CURP.
            gender (Gender): masculino or femenino.
            birthday (datetime.date): Date of birth.
            search_type (SearchType): fisica or moral.
            search_list (tuple[SearchList, ...]): Lists to search.
               If not provided, searches all.

            The search is hierarchical: it first looks for a match by RFC,
            then by CURP if RFC is not found, and finally by name if
            neither is found.

        """
        # Validate search criteria
        by_name = full_name is not None
        by_rfc = rfc is not None
        by_curp = curp is not None

        if not (by_name or by_rfc or by_curp):
            raise InvalidSearchCriteriaError

        token = await self._fetch_auth_token()

        # Build base URL with required parameters
        search_url = f'{self.base_url}/api/find'

        params: dict[str, str | int | None] = {
            'client_id': self.client_id,
            'username': self.username,
            'percent': match_score,
        }

        if by_name:
            params['name'] = full_name
        if rfc:
            params['rfc'] = rfc
        if curp:
            params['curp'] = curp
        if gender:
            params['sex'] = gender
        if birthday:
            params['birthday'] = birthday.strftime('%d/%m/%Y')
        if search_type is not None:
            params['type'] = search_type
        if search_list:
            params['list'] = ','.join(search_list)

        headers = {'Authorization': f'Bearer {token}'}

        try:
            response = await self._make_request(
                'GET', search_url, params=params, headers=headers
            )
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 401:
                self._invalidate_auth_token()
                raise InvalidTokenError(response)
            raise QuienEsQuienError(response)

        response_data = response.json()
        if not response_data.get('success', False):
            status = response_data.get('status', '')
            if status == NOT_FOUND_ERROR_RESPONSE:
                raise PersonNotFoundError(response)
            if status == INVALID_TOKEN_ERROR_RESPONSE:
                self._invalidate_auth_token()
                raise InvalidTokenError(response)
            if status == INVALID_PLAN_ERROR_RESPONSE:
                raise InvalidPlanError(response)
            if status == INSUFFICIENT_BALANCE_ERROR_RESPONSE:
                raise InsufficientBalanceError(response)
            raise QuienEsQuienError(response)

        matched_persons = [
            Person(**person_data)
            for person_data in response_data.get('data', [])
        ]

        return matched_persons
