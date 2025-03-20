import io
import zipfile

import httpx

from utils.httpx_client import client, retry_on_httpx


@retry_on_httpx
async def download(url: str) -> bytes:
    """
    Asynchronously downloads a ZIP file from the given URL.
    :param url: The URL to fetch the ZIP file from.
    :return: The content of the ZIP file in bytes.
    """
    response = await client.get(url)
    response.raise_for_status()

    if not response.content:
        raise httpx.HTTPStatusError(
            "Empty response received", request=response.request, response=response
        )

    return response.content


def extract_content(zip_content: bytes) -> io.StringIO:
    """
    Extracts the CSV content from a ZIP file.
    :param zip_content: The ZIP file content in bytes.
    :return: A StringIO object containing the CSV content.
    """
    with zipfile.ZipFile(io.BytesIO(zip_content), "r") as z:
        file_names = z.namelist()
        if not file_names:
            raise ValueError("ZIP file is empty")
        file_name = file_names[0]
        with z.open(file_name) as f:
            return io.StringIO(f.read().decode("utf-8"))
