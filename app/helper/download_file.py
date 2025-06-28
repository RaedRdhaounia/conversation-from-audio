import aiohttp
import aiofiles
import os
import tempfile
import uuid

async def download_file(url: str) -> str:
    """
    Asynchronously downloads a file from the specified URL and saves it to a temporary location.

    Args:
        url (str): The URL of the file to download.

    Returns:
        str: The file path of the saved temporary file.

    Raises:
        aiohttp.ClientResponseError: If the HTTP request fails (e.g., 404, 500).
        aiohttp.ClientError: For other client-side errors during the HTTP request.

    Notes:
        - The file is saved with a unique filename using UUID in the system temporary directory.
        - Uses aiohttp for asynchronous HTTP requests and aiofiles for asynchronous file writing.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            resp.raise_for_status()
            data = await resp.read()

    temp_dir = tempfile.gettempdir()
    unique_filename = f"{uuid.uuid4()}.mp3"
    tmp_path = os.path.join(temp_dir, unique_filename)

    async with aiofiles.open(tmp_path, 'wb') as tmp_file:
        await tmp_file.write(data)

    return tmp_path
