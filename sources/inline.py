"""Templates of messages for inline query."""

from telethon.tl.custom import Button


INLINE_MESSAGES = {
    'start': {
        'message':
"""Для начала сбора данных выберите промежуток даты

<b>Дата начала:</b> {day_start}.{month_start}.{year_start}
<b>Дата окончания:</b> {day_end}.{month_end}.{year_end}""",
        'buttons': [
            [Button.inline('Выбрать дату старта', b'date_start')],
            [Button.inline('Выбрать дату окончания', b'date_end')],
            [Button.inline('Начать сбор базы', b'start')]
        ]
    },

    'input_day': {
        'message': 'Выберите день из предложенных ниже',
        'buttons': [
            [
                Button.inline('1', b'day:1'),
                Button.inline('2', b'day:2'),
                Button.inline('3', b'day:3'),
                Button.inline('4', b'day:4'),
                Button.inline('5', b'day:5'),
                Button.inline('6', b'day:6'),
                Button.inline('7', b'day:7'),
                Button.inline('8', b'day:8'),
            ],
            [
                Button.inline('9', b'day:9'),
                Button.inline('10', b'day:10'),
                Button.inline('11', b'day:11'),
                Button.inline('12', b'day:12'),
                Button.inline('13', b'day:13'),
                Button.inline('14', b'day:14'),
                Button.inline('15', b'day:15'),
                Button.inline('16', b'day:16'),
            ],
            [
                Button.inline('17', b'day:17'),
                Button.inline('18', b'day:18'),
                Button.inline('19', b'day:19'),
                Button.inline('20', b'day:20'),
                Button.inline('21', b'day:21'),
                Button.inline('22', b'day:22'),
                Button.inline('23', b'day:23'),
                Button.inline('24', b'day:24'),
            ],
            [
                Button.inline('25', b'day:25'),
                Button.inline('26', b'day:26'),
                Button.inline('27', b'day:27'),
                Button.inline('28', b'day:28'),
                Button.inline('29', b'day:29'),
                Button.inline('30', b'day:30'),
                Button.inline('31', b'day:31')
            ]
        ]
    },

    'input_month': {
        'message': 'Выберите месяц из предложеных ниже',
        'buttons': [
            [
                Button.inline('Январь', b'month:1'),
                Button.inline('Февраль', b'month:2'),
                Button.inline('Март', b'month:3'),
            ],
            [
                Button.inline('Апрель', b'month:4'),
                Button.inline('Май', b'month:5'),
                Button.inline('Июнь', b'month:6'),
            ],
            [
                Button.inline('Июль', b'month:7'),
                Button.inline('Август', b'month:8'),
                Button.inline('Сентябрь', b'month:9'),
            ],
            [
                Button.inline('Октябрь', b'month:10'),
                Button.inline('Ноябрь', b'month:11'),
                Button.inline('Декабрь', b'month:12'),
            ],
        ]
    },

    'input_year': {
        'message': 'Выберите год из предложенных ниже',
        'buttons': [
            Button.inline('2022', b'year:2022'),
            Button.inline('2023', b'year:2023'),
            Button.inline('2024', b'year:2024'),
        ]
    }
}


MESSAGES = {
    'base_begin': 'Сбор базы данных начался. Ее уникальный идентификатор {}',
    'base_end': 'База данных успешно собрана. Файл {}',
    'base_failed': 'Не найдено ни одного сообщения в указанные даты'
}
