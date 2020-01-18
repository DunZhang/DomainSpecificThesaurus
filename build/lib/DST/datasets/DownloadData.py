import requests
import zipfile
import warnings
from sys import stdout
from os import makedirs
from os.path import dirname
from os.path import exists
import logging

logger = logging.getLogger(__name__)

class GoogleDriveDownloader:
    """
    Minimal class to download shared files from Google Drive.
    """

    CHUNK_SIZE = 32768
    DOWNLOAD_URL = "https://docs.google.com/uc?export=download"

    @staticmethod
    def download_file_from_google_drive(file_id, dest_path, overwrite=False, unzip=False):
        """
        Downloads a shared file from google drive into a given folder.
        Optionally unzips it.
        Parameters
        ----------
        file_id: str
            the file identifier.
            You can obtain it from the sharable link.
        dest_path: str
            the destination where to save the downloaded file.
            Must be a path (for example: './downloaded_file.txt')
        overwrite: bool
            optional, if True forces re-download and overwrite.
        unzip: bool
            optional, if True unzips a file.
            If the file is not a zip file, ignores it.
        Returns
        -------
        None
        """

        destination_directory = dirname(dest_path)
        if not exists(destination_directory):
            makedirs(destination_directory)

        if not exists(dest_path) or overwrite:

            session = requests.Session()

            logger.info('Downloading {} into {}... '.format(file_id, dest_path))
            stdout.flush()

            response = session.get(GoogleDriveDownloader.DOWNLOAD_URL, params={'id': file_id}, stream=True)

            token = GoogleDriveDownloader._get_confirm_token(response)
            if token:
                params = {'id': file_id, 'confirm': token}
                response = session.get(GoogleDriveDownloader.DOWNLOAD_URL, params=params, stream=True)

            GoogleDriveDownloader._save_response_content(response, dest_path)
            logger.info('Finish download')

            if unzip:
                try:
                    logger.info('Unzipping...')
                    stdout.flush()
                    with zipfile.ZipFile(dest_path, 'r') as z:
                        z.extractall(destination_directory)
                        logger.info('Finish unzip.')
                except zipfile.BadZipfile:
                    warnings.warn('Ignoring `unzip` since "{}" does not look like a valid zip file'.format(file_id))

    @staticmethod
    def _get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value
        return None

    @staticmethod
    def _save_response_content(response, destination):
        with open(destination, "wb") as f:
            for chunk in response.iter_content(GoogleDriveDownloader.CHUNK_SIZE):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)


class DownloadData():
    def __init__(self):
        self.fileId = {
            "test": "17uxLDQu1tOqHG6XZ7AiKabvAIY-iwJnF",
            "general_vocab": "1SJonZ_-ns8HKAqsHCgswHssXlUNyX9gW",
            "eng_corpus": "1ez1riFK_EDNfnHBwK7zLhXLUcYD7uYTh",
        }

    def download_data(self, dest_path, download_file_name="test", overwrite=False):
        GoogleDriveDownloader.download_file_from_google_drive(file_id=self.fileId[download_file_name], dest_path=dest_path,
                                                              overwrite=overwrite, unzip=True)


if __name__ == "__main__":
    pass
