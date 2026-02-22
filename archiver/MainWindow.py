import time
from datetime import datetime

import FreeSimpleGUI as sg

import Core
import File

sizeX = 600
sizeY = 400

compress_result = {}
icon_path = '../data/arch.png'
options = {
    'chunk_size': 4096,
    'file_path': "",
    'suffix_file': '_sar_',
    'postfix_file': '.sar'
}


def main_wind():
    """
    Основное окно
    """
    sg.theme('Light Green')
    menu_def = [['&Меню', ['&Архивировать файл', '&Распаковать файл', '&Очистить поле']],
                ['&Инструменты', ['&Сравнить файлы', '&Изменить настройки архивации']],
                ['&О программе', ['&Информация']]]
    layout = [[sg.Menu(menu_def, tearoff=False)],
              [sg.Multiline(size=(70, 20), key='out_date', disabled=True, autoscroll=True, font=('Courier New', 14),
                            default_text='/* Добро пожаловать в программу Архиватор! *\\\n\n')]]
    window = sg.Window('Архиватор', layout, size=(sizeX, sizeY), icon=icon_path)
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Quit'):
            break
        menu_event(event, window)
    window.close()


def menu_event(event, main_window):
    """
    Обработка событий меню

    :param event: Название события (текст на кнопке)
    :param main_window: Объект текущего (главного) окна FreeSimpleGUI
    """
    if event == 'Архивировать файл':
        compress_event(main_window)
    if event == 'Распаковать файл':
        decompress_event(main_window)
    if event == 'Очистить поле':
        clear_out_date(main_window)
    if event == 'Изменить настройки архивации':
        change_tools(main_window)
    if event == 'Сравнить файлы':
        check_files(main_window)
    if event == 'Информация':
        window_info_event(main_window)


def compress_event(window):
    """Архивировать файл"""
    print_info(window, 'Загрузка файла...')
    temp_path = sg.popup_get_file('Выберите файл для загрузки', no_window=True, icon=icon_path)
    if not temp_path:
        print_info(window, 'Файл не загружен.')
        sg.popup_ok('Файл не загружен', icon=icon_path)
        return
    options['file_path'] = temp_path
    data_chunks = []
    chunk_len = 0
    for chunk in File.read_chunks(options):
        data_chunks.append(chunk)
        chunk_len += len(chunk)
    print_info(window, f'Файл загружен. Блоков: {len(data_chunks)}. Размер данных: {human_size(chunk_len)}.\n')
    print_info(window, f'Старт архивации файла в {time.strftime("%H:%M:%S")} ...')
    start_time = time.perf_counter()
    is_compress = Core.compress_data(data_chunks, options)
    end_time = time.perf_counter() - start_time
    print_info(window, f'... Завершено в {time.strftime("%H:%M:%S")}.')
    if is_compress:
        data_chunks.clear()
        print_info(window, f'Файл упакован за {format_time(end_time)}')
        sg.popup_ok('Файл успешно запакован!', icon=icon_path)
    else:
        print_info(window, 'Ошибка архивации!')
        sg.popup_error('Ошибка архивации!', icon=icon_path)


def decompress_event(window):
    """Распаковать файл"""
    print_info(window, 'Загрузка файла для распаковки...')
    temp_path = sg.popup_get_file('Выберите файл для распаковки', no_window=True, icon=icon_path)
    if temp_path:
        options['file_path'] = temp_path
        print_info(window, f'Старт распаковки файла в {time.strftime("%H:%M:%S")} ...')
        start_time = time.perf_counter()
        is_decompress = Core.decompress_data(options)
        end_time = time.perf_counter() - start_time
        print_info(window, f'... Завершено в {time.strftime("%H:%M:%S")}.')
        if is_decompress:
            print_info(window, f'Файл распакован за {format_time(end_time)}')
            sg.popup_ok('Файл успешно распакован!', icon=icon_path)
        else:
            print_info(window, 'Ошибка распаковки!')
            sg.popup_error('Ошибка распаковки!', icon=icon_path)
    else:
        print_info(window, 'Файл не загружен.')
        sg.popup_ok('Файл не загружен', icon=icon_path)


def window_info_event(main_window):
    """Отображает информацию о программе Архиватор."""
    sg.theme('Light Green')
    info_text = (
        "\t/* О программе Архиватор! */\n\n"
        "Версия: always the latest version... or so I tell myself 🤪💻\n\n"
        "Разработчик: 10% coding, 90% googling 🤓🔍\n\n"
        "Описание: Магия сжатия по алгоритму Хаффмана. \n"
        "Ни один байт при разработке не пострадал! 🧙‍♂️📦"
    )
    layout = [
        [sg.Multiline(info_text, size=(45, 10), key='-INFO-', disabled=True, font=('Courier New', 12),
                      no_scrollbar=True, border_width=0)],
        [sg.Button('Закрыть', size=(10, 1))]
    ]
    print_info(main_window, "Информация о программе Архиватор.")
    info_window = sg.Window('Информация', layout, modal=True, element_justification='c', icon=icon_path)
    while True:
        event, values = info_window.read()
        if event in (sg.WIN_CLOSED, 'Закрыть'):
            break
    info_window.close()


def change_tools(main_window):
    """Изменить настройки архиватора"""
    sg.theme('Light Green')
    chunk_options = {
        '1 KB': 1024, '2 KB': 2048, '4 KB (Стандарт)': 4096,
        '8 KB': 8192, '16 KB': 16384, '32 KB': 32768,
        '64 KB': 65536, '128 KB': 131072, '256 KB': 262144,
        '512 KB': 524288, '1 MB': 1048576, '2 MB': 2097152, '4 MB': 4194304
    }
    current_chunk_label = next((k for k, v in chunk_options.items() if v == options['chunk_size']), '4 KB (Стандарт)')
    layout = [
        [sg.Text('Настройки именования файлов', font=('Helvetica', 10, 'bold'))],
        [sg.Text('Суффикс (в середине):'), sg.Input(options['suffix_file'], key='-SUFFIX-', size=(15, 1))],
        [sg.Text('Постфикс (расширение):'), sg.Input(options['postfix_file'], key='-POSTFIX-', size=(15, 1))],
        [sg.HorizontalSeparator(pad=(0, 15))],
        [sg.Text('Производительность', font=('Helvetica', 10, 'bold'))],
        [sg.Text('Размер чанка для чтения:')],
        [sg.Combo(list(chunk_options.keys()),
                  default_value=current_chunk_label,
                  key='-CHUNK-',
                  readonly=True,
                  size=(20, 1))],
        [sg.Button('Применить', size=(12, 1), button_color=('white', '#28a745')),
         sg.Button('Закрыть', size=(10, 1))]
    ]
    info_window = sg.Window('Изменение настроек архиватора', layout, modal=True,
                            element_justification='r', icon=icon_path)
    while True:
        event, values = info_window.read()
        if event == 'Применить':
            selected_label = values['-CHUNK-']
            options['chunk_size'] = chunk_options[selected_label]
            options['suffix_file'] = values['-SUFFIX-']
            options['postfix_file'] = values['-POSTFIX-']
            print_info(main_window, "Настройки обновлены:")
            print_info(main_window, f"Суффикс (в середине) при распаковке: {options['suffix_file']}")
            print_info(main_window, f"Расширение: {options['postfix_file']}")
            print_info(main_window, f"Блоки считывания файла: {human_size(options['chunk_size'])}")
        if event in (sg.WIN_CLOSED, 'Закрыть'):
            break
    info_window.close()


def check_files(main_window):
    """Сравнить файлы hash md5"""
    sg.theme('Light Green')
    layout = [
        [sg.Text('Выберите файлы для сравнения (MD5):', font=('Helvetica', 12, 'bold'))],
        [sg.Text('Файл 1:', size=(8, 1)), sg.Input(key='-FILE1-'), sg.FileBrowse('Обзор')],
        [sg.Text('Файл 2:', size=(8, 1)), sg.Input(key='-FILE2-'), sg.FileBrowse('Обзор')],
        [sg.HorizontalSeparator(pad=(0, 15))],
        [sg.Button('Сравнить', size=(12, 1), button_color='green'),
         sg.Button('Закрыть', size=(10, 1))]
    ]
    check_window = sg.Window('Проверка целостности', layout, modal=True, icon=icon_path)
    while True:
        event, values = check_window.read()
        if event in (sg.WIN_CLOSED, 'Закрыть'):
            break
        if event == 'Сравнить':
            f1, f2 = values['-FILE1-'], values['-FILE2-']
            if not f1 or not f2:
                sg.popup_error('Выберите оба файла!', icon=icon_path)
                continue
            print_info(main_window, "Запущено сравнение файлов...")
            h1 = File.get_file_hash(f1, options.get('chunk_size', 4096))
            h2 = File.get_file_hash(f2, options.get('chunk_size', 4096))
            if "Error" in h1 or "Error" in h2:
                sg.popup_error(f"Ошибка при чтении файлов:\nF1: {h1}\nF2: {h2}", icon=icon_path)
                print_info(main_window, f"Ошибка при чтении файлов:\nF1: {h1}\nF2: {h2}")
            elif h1 == h2:
                print_info(main_window, f"Результат: Файлы идентичны ✅\nMD5: {h1}")
                sg.popup("✅ Успех!", "Файлы абсолютно идентичны.", f"MD5: {h1}", icon=icon_path)
            else:
                print_info(main_window, f"Результат: Файлы РАЗЛИЧАЮТСЯ ❌")
                sg.popup_error("❌ Ошибка!", "Файлы различаются!", f"F1: {h1}", f"F2: {h2}", icon=icon_path)

    check_window.close()


def print_info(window, message):
    current_time = datetime.now().strftime("%H:%M:%S")
    window['out_date'].update(f"[{current_time}] {message}\n", append=True)


def clear_out_date(window):
    window['out_date'].update('')


def human_size(size):
    units = ['Б', 'КБ', 'МБ', 'ГБ']
    for unit in units:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return "> 1 TБ"


def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    if minutes > 0:
        return f"{int(minutes)} мин {seconds:.2f} сек"
    return f"{seconds:.2f} сек"


if __name__ == '__main__':
    main_wind()
