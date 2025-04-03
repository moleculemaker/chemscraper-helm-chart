from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    index_name: Union[Unset, str] = "",
    text_query: Union[Unset, str] = "",
    smiles_query: Union[Unset, str] = "",
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["index_name"] = index_name

    params["text_query"] = text_query

    params["smiles_query"] = smiles_query

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/search",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = response.json()
        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    index_name: Union[Unset, str] = "",
    text_query: Union[Unset, str] = "",
    smiles_query: Union[Unset, str] = "",
) -> Response[Union[Any, HTTPValidationError]]:
    """Search

    Args:
        index_name (Union[Unset, str]):  Default: ''.
        text_query (Union[Unset, str]):  Default: ''.
        smiles_query (Union[Unset, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        index_name=index_name,
        text_query=text_query,
        smiles_query=smiles_query,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    index_name: Union[Unset, str] = "",
    text_query: Union[Unset, str] = "",
    smiles_query: Union[Unset, str] = "",
) -> Optional[Union[Any, HTTPValidationError]]:
    """Search

    Args:
        index_name (Union[Unset, str]):  Default: ''.
        text_query (Union[Unset, str]):  Default: ''.
        smiles_query (Union[Unset, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return sync_detailed(
        client=client,
        index_name=index_name,
        text_query=text_query,
        smiles_query=smiles_query,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    index_name: Union[Unset, str] = "",
    text_query: Union[Unset, str] = "",
    smiles_query: Union[Unset, str] = "",
) -> Response[Union[Any, HTTPValidationError]]:
    """Search

    Args:
        index_name (Union[Unset, str]):  Default: ''.
        text_query (Union[Unset, str]):  Default: ''.
        smiles_query (Union[Unset, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        index_name=index_name,
        text_query=text_query,
        smiles_query=smiles_query,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    index_name: Union[Unset, str] = "",
    text_query: Union[Unset, str] = "",
    smiles_query: Union[Unset, str] = "",
) -> Optional[Union[Any, HTTPValidationError]]:
    """Search

    Args:
        index_name (Union[Unset, str]):  Default: ''.
        text_query (Union[Unset, str]):  Default: ''.
        smiles_query (Union[Unset, str]):  Default: ''.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            client=client,
            index_name=index_name,
            text_query=text_query,
            smiles_query=smiles_query,
        )
    ).parsed
