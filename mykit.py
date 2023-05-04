from hashlib import new


def ct(*message, **kwargs): #Форматирование текста в консоли (color(c), background(b), effect(e))
    """
    Каждый парамерт может быть равен от 0 до 7

    color;
    background;
    effect;
    """

    text = ''
    for key in kwargs:
        if key == 'color' or key == 'c' or key == 'с':
            kwargs[key] = min(7, kwargs[key])
            text += f'\033[{kwargs[key]+30}m'
        elif key == 'background' or key == 'b' or key == 'ф':
            kwargs[key] = min(7, kwargs[key])
            text += f'\033[{kwargs[key]+40}m'
        elif key == 'effect' or key == 'e' or key == 'э':
            kwargs[key] = min(7, kwargs[key])
            text += f'\033[{kwargs[key]}m'

    if len(message) > 1: #Пробелы
        for i in message:
            if message[len(message)-1] == i:
                text += i
            else:
                text += i + " "
    else:
        text += message[0]
    
    text += '\033[0m'
    return text
def get_date():
    import datetime

    dt_now = datetime.datetime.now()
    return str(dt_now.date()).replace('-', ".")
def get_time():
    import datetime

    dt_now = datetime.datetime.now()
    return str(dt_now.time())
def error(err):
    print(ct("ОШИБКА", c=1) + ":", ct(str(err), c=4))
    return (ct("ОШИБКА", c=1) + ":", ct(str(err), c=4))
def get_current_function(func):
    print(func)
    return func
def hex_rgb(HEX):
    """
    Пример: hex_rgb(HEX)
    HEX - Строчный, обязателен символ "#"
    """
    try:
        if HEX[0] == "#":
            return tuple(int(HEX[1:][i:i+2], 16) for i in (0, 2, 4))
        else:
            error("По-моему это не HEXcode")
            return "По-моему это не HEXcode"
        
    except Exception as err:
        print(err)
        return err
def rgb_hex(rgb, sym="#"):
    """
    Пример: rgb_hex( (r, g, b), sym )
    Сначала в кортеже вводим нужные нам числа (Все от 0 до 255), потом идёт симол, который поставится в начале, по-умолчанию - это "#"
    """
    return f"{sym}" + ('%02x%02x%02x' % rgb).upper()



def help():
    print(ct('MyKit - Лев Бутаков', c=6))
    print(ct('-------------------------------', c=3))
    print(ct('Функция ', c=5) + ct('"ct (FormatText)"', c=1) + ":", ct("Активна", c=2))
    print(ct('Функция ', c=5) + ct('"get_date"', c=1) + ":", ct("Активна", c=2))
    print(ct('Функция ', c=5) + ct('"get_time"', c=1) + ":", ct("Активна", c=2))
    print(ct('Функция ', c=5) + ct('"get_current_function"', c=1) + ":", ct("Активна", c=2))
    print(ct('Функция ', c=5) + ct('"hex_rgb"', c=1) + ":", ct("Активна", c=2))
    print(ct('Функция ', c=5) + ct('"rgb_hex"', c=1) + ":", ct("Активна", c=2))
    print(ct('-------------------------------', c=3))

if __name__ == '__main__':
    help()
    