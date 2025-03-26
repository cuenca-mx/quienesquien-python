import datetime as dt
from dataclasses import dataclass
from typing import Any, ClassVar, Mapping

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


@dataclass
class Client:
    base_url = 'https://app.q-detect.com'
    username: str
    auth_token: str | None = None
    _client: ClassVar[httpx.AsyncClient] = httpx.AsyncClient()

    async def _make_request(
        self,
        method: str,
        url: str,
        *,
        headers: Mapping[str, str] | None = None,
        params: Mapping[str, Any] | None = None,
    ) -> httpx.Response:
        """Make an HTTP request using an async client."""
        response = await self._client.request(
            method, url, headers=headers, params=params
        )
        response.raise_for_status()
        return response

    @classmethod
    async def create_token(cls, client_id: str, secret_key: str) -> str:
        """Create a new authentication token."""
        auth_url = f'{cls.base_url}/api/token'
        params = {'client_id': client_id}
        headers = {
            'Authorization': f'Bearer {secret_key}',
            'Accept-Encoding': 'identity',
        }
        try:
            response = await cls._client.request(
                'GET', auth_url, headers=headers, params=params
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise QuienEsQuienError(exc.response) from exc
        return response.text

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
        assert (
            self.auth_token
        ), 'you must create or reuse an already created auth token'

        if not (full_name or rfc or curp):
            raise InvalidSearchCriteriaError

        # Build base URL with required parameters
        search_url = f'{self.base_url}/api/find'

        params = {
            'username': self.username,
            'percent': match_score,
            'name': full_name,
            'rfc': rfc,
            'curp': curp,
            'sex': gender.value if gender else None,
            'birthday': birthday.strftime('%d/%m/%Y') if birthday else None,
            'type': search_type.value if search_type is not None else None,
            'list': ','.join(search_list) if search_list else None,
        }

        params = {k: v for k, v in params.items() if v is not None}

        headers = {'Authorization': f'Bearer {self.auth_token}'}

        try:
            response = await self._make_request(
                'GET', search_url, params=params, headers=headers
            )
        except httpx.HTTPStatusError as exc:
            match exc.response.status_code:
                case 401:
                    raise InvalidTokenError(exc.response)
                case 403:
                    raise InsufficientBalanceError(exc.response)
                case _:
                    raise QuienEsQuienError(exc.response) from exc

        response_data = response.json()
        if not response_data.get('success', False):
            status = response_data.get('status', '')
            match status:
                case 'No se han encontrado coincidencias':
                    raise PersonNotFoundError(response)
                case (
                    'El token proporcionado para realizar esta acción '
                    'es inválido'
                ):
                    raise InvalidTokenError(response)
                case (
                    'Tu plan de consultas ha expirado, por favor '
                    'actualiza tu plan para continuar usando la API'
                ):
                    raise InvalidPlanError(response)
                case _:
                    raise QuienEsQuienError(response)

        matched_persons = [
            Person(**person_data)
            for person_data in response_data.get('data', [])
        ]

        return matched_persons
