import speech_recognition
import webbrowser

from subprocess import Popen

sr = speech_recognition.Recognizer()
sr.pause_threshold = 0.5

available_sites = {
    'browsers': {
        'youtube': 'https://www.youtube.com/',
        'вконтакте': 'https://vk.com/feed',
        'гитхаб': 'https://github.com/',
        'instagram': 'https://www.instagram.com/',
        'реддит': 'https://www.reddit.com/'
    }
}
command_dict = {
    'commands': {
        'greeting': ['привет', 'хай', 'здорово', 'приветствую'],
        'create_task': ['добавить задачу', 'создать задачу', 'добавить задание', 'добавить запись',
                        'добавить'],
        'delete_task': ['удалить задачу', 'удалить запись', 'удалить'],
        'open_browse': ['открыть браузер', 'запустить браузер'],
        'close_browse': ['закрыть браузер']
    }
}


def command_recognition():
    """check for errors"""
    try:
        with speech_recognition.Microphone() as mic:
            sr.adjust_for_ambient_noise(source=mic, duration=0.5)
            audio = sr.listen(source=mic)
            query = sr.recognize_google(audio_data=audio, language='ru-RU').lower()
        return query
    except speech_recognition.UnknownValueError:
        return 'Я не смог тебя понять' and main()


def main():
    while True:
        query = command_recognition()
        for key, value in command_dict['commands'].items():
            if query in value:
                print(globals()[key]())
        if query == 'стоп':
            exit()


def create_task():
    print('Говорите что добавить: ')
    query = command_recognition()

    with open('ToDo_list.txt', 'a', encoding='utf-8') as f:
        f.write(f'\n{query}')

    return f'"{query}" - добавлено'


def delete_task():
    print('Что вы хотите удалить:')
    query = command_recognition()

    new_l = []

    with open('ToDo_list.txt', 'r', encoding='utf-8') as f:
        for line in f:
            new_l.append(line.strip())

    with open('ToDo_list.txt', 'w', encoding='utf-8') as f:
        if query in new_l:
            new_l.remove(query)
        else:
            f.write('\n'.join(new_l))
            return 'Такого нет'
        f.write('\n'.join(new_l))
    return f'"{query}" - успешно удалено'


def open_browse():
    print('Можно открыть несколько сайтов \n'
          'Выберете какой вы хотите \n'
          'Сайты которые можно открыть: youtube, vk, github, instagram, reddit')
    query = command_recognition()
    for key, value in available_sites['browsers'].items():
        if query in key:
            webbrowser.open(value)
            return f'{value} открыт'


def close_browse():
    print('Скажите "закрыть"')
    query = command_recognition()
    if query == 'закрыть':
        Popen('taskkill /F /IM chrome.exe', shell=True)
        return 'Браузер был закрыт'


def greeting():
    return 'ну здарово'


if __name__ == '__main__':
    main()
