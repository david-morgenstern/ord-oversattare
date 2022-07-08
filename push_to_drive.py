from authenticate import drive_service
from googleapiclient.http import MediaFileUpload


def push_to_drive():
    service = drive_service()
    file_name = 'swedish_spreadsheet.xlsx'

    try:
        file_metadata = {
            'name': file_name,
            'mimeType': 'application/vnd.google-apps.spreadsheet'
        }
        for file in service.files().list(q=f"name='{file_name}'").execute()['files']:
            service.files().delete(fileId=file['id']).execute()

        media = MediaFileUpload('done.xlsx', mimetype='application/x-vnd.oasis.opendocument.spreadsheet')
        file = service.files().create(
            media_body=media,
            body=file_metadata
        ).execute()

        print(file)
        return file
    except Exception as e:
        print(e)


if __name__ == "__main__":
    push_to_drive()
