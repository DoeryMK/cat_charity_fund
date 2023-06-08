import copy
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.core.consts import FORMAT
from app.services.exceptions import InvalidTableSize

REPORT_NAME = 'Отчет от {current_date_time}'
REPORT_SHEETS_LOCALE = 'ru_RU'
REPORT_SHEETS_TITLE = 'Лист1'
REPORT_SHEETS_TYPE = 'GRID'

REPORT_SHEETS_COLUMNS_NUMBER = 5
REPORT_SHEETS_ROWS_NUMBER = 100
UPDATE_RANGE = 'R1C1:R{row_number}C{column_number}'

REPORT_SHEETS_PROPERTIES = dict(
    sheetType=REPORT_SHEETS_TYPE,
    sheetId=0,
    title=REPORT_SHEETS_TITLE,
    gridProperties=dict(
        rowCount=REPORT_SHEETS_ROWS_NUMBER,
        columnCount=REPORT_SHEETS_COLUMNS_NUMBER,
    )
)

SPREADSHEET_BODY = dict(
    properties=dict(
        title=REPORT_NAME,
        locale=REPORT_SHEETS_LOCALE
    ),
    sheets=[dict(
        properties=REPORT_SHEETS_PROPERTIES
    )]
)

TABLE_HEAD = (
    ['Отчет от'],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
)

COLUMNS_QUANTITY_NOT_ENOUGH = (
    'Размер сформированного отчета не соответствует '
    'габаритам созданной таблицы. '
    'Допустимое количество столбцов таблицы - '
    f'{REPORT_SHEETS_COLUMNS_NUMBER}. '
    'Количество столбцов в отчете - {current_columns_number}.'
)
ROWS_QUANTITY_NOT_ENOUGH = (
    'Размер сформированного отчета не соответствует '
    'габаритам созданной таблицы. '
    'Допустимое количество строк таблицы - '
    f'{REPORT_SHEETS_ROWS_NUMBER}. '
    'Количество строк в отчете - {current_rows_number}.'
)


async def spreadsheets_create(
        wrapper_services: Aiogoogle,
        spreadsheet_body: Optional[Dict] = None
) -> str:
    service = await wrapper_services.discover('sheets', 'v4')
    if not spreadsheet_body:
        spreadsheet_body = copy.deepcopy(SPREADSHEET_BODY)
    spreadsheet_body['properties']['title'] = REPORT_NAME.format(
        current_date_time=datetime.now().strftime(FORMAT)
    )
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(
            json=spreadsheet_body
        )
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email
    }
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields="id",
        )
    )


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: List,
        wrapper_services: Aiogoogle

) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    table_head = copy.deepcopy(TABLE_HEAD)
    table_head[0].append(datetime.now().strftime(FORMAT))
    table_values = [
        *table_head,
        *[list(map(
            lambda x: str(timedelta(x)) if isinstance(x, float) else x, project
        )) for project in projects]
    ]
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    current_rows_number = len(table_values)
    current_columns_number = max(map(len, table_values))
    if current_rows_number > REPORT_SHEETS_ROWS_NUMBER:
        raise InvalidTableSize(
            ROWS_QUANTITY_NOT_ENOUGH.format(
                current_rows_number=current_rows_number
            )
        )
    if current_columns_number > REPORT_SHEETS_COLUMNS_NUMBER:
        raise InvalidTableSize(
            COLUMNS_QUANTITY_NOT_ENOUGH.format(
                current_columns_number=current_columns_number
            )
        )
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=UPDATE_RANGE.format(
                row_number=current_rows_number,
                column_number=current_columns_number
            ),
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
