# Начальная матрица перестановки для данных
PI = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

# Начальная перестановка ключа
CP_1 = [57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4]

# Перестановка после сдвига ключа для получения Ki+1
CP_2 = [14, 17, 11, 24, 1, 5, 3, 28,
        15, 6, 21, 10, 23, 19, 12, 4,
        26, 8, 16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55, 30, 40,
        51, 45, 33, 48, 44, 49, 39, 56,
        34, 53, 46, 42, 50, 36, 29, 32]

# Матрица расширения для получения 48-битовой матрицы данных для применения xor с Ki
E = [32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32, 1]

# SBOX
S_BOX = [
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]],
]

# Перестановка после каждой замены S-блока для каждого раунда
P = [16, 7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9,
     19, 13, 30, 6, 22, 11, 4, 25]

# Конечная перестановка для данных после 16 раундов
PI_1 = [40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25]

# Матрица, определяющая сдвиг для каждого раунда ключей
SHIFT = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]


def string_to_bit_array(text):
    return [int(bit) for char in text for bit in '{:08b}'.format(ord(char))]


def bit_array_to_string(array):
    return ''.join(chr(int(''.join(map(str, array[i:i+8])), 2)) for i in range(0, len(array), 8))


def binvalue(val, bitsize): # Возвращает двоичное значение как строку заданного размера
    if isinstance(val, int):
        binval = bin(val)[2:]
    else:
        binval = bin(ord(val))[2:]

    binval = binval.zfill(bitsize)  # Заполнение нулями до нужной длины
    if len(binval) > bitsize:
        raise ValueError("binary value larger than the expected size")

    return binval


def nsplit(s, n):  # Разбиение списка на подсписки размером "n"
    return [s[i:i + n] for i in range(0, len(s), n)]


ENCRYPT = 1
DECRYPT = 0


class Des():
    def __init__(self):
        self.password = None
        self.text = None
        self.keys = list()

    def run(self, key, text, action=ENCRYPT, padding=False):
        key = self.validate_key(key)
        self.password = key[:8]
        self.text = text

        if padding and action == ENCRYPT:
            self.addPadding()
        elif len(self.text) % 8 != 0: # Если не указана дополнительная информация о размере, размер данных должен быть кратным 8 байтам
            raise Exception("Data size should be multiple of 8")

        self.generatekeys() # Генерация всех ключей
        text_blocks = nsplit(self.text, 8) # Разбиение текста на блоки по 8 байт, то есть 64 бита
        result = []

        for block in text_blocks: # Цикл по всем блокам данных
            block = string_to_bit_array(block)
            block = self.permut(block, PI) # Применение начальной перестановки
            g, d = nsplit(block, 32)
            tmp = None

            for i in range(16): # 16 раундов
                d_e = self.expand(d, E)   # Расширение d до размера Ki (48 бит)

                if action == ENCRYPT:
                    tmp = self.xor(self.keys[i], d_e) # Если шифрование, использовать Ki
                else:
                    tmp = self.xor(self.keys[15 - i], d_e) # Если дешифрование, начать с последнего ключа

                tmp = self.substitute(tmp) # Применение S-блоков
                tmp = self.permut(tmp, P)
                tmp = self.xor(g, tmp)
                g = d
                d = tmp

            result += self.permut(d + g, PI_1) # Последняя перестановка и добавление результата

        final_res = bit_array_to_string(result)

        if padding and action == DECRYPT:
            return self.removePadding(final_res) # Удаление дополнения, если выполняется дешифрование и дополнение включено
        else:
            return final_res # Возврат конечной строки данных

    def substitute(self, d_e):  # Цикл по всем подспискам
        result = []

        for i, block in enumerate(nsplit(d_e, 6)):
            row = int(str(block[0]) + str(block[5]), 2)  # Получение строки с первым и последним битом
            column = int(''.join(map(str, block[1:5])), 2)  # Столбец - 2, 3, 4, 5 биты
            val = S_BOX[i][row][column]  # Получение значения в соответствующем S-блоке (i)
            result.extend(map(int, binvalue(val, 4)))  # Добавление в результирующий список

        return result

    def permut(self, block, table):  # Перестановка блока по заданной таблице (универсальный метод)
        return [block[x - 1] for x in table]

    def expand(self, block, table):  # То же, что и permut, но для ясности переименован
        return [block[x - 1] for x in table]

    def xor(self, t1, t2):  # Применение XOR и возврат результата
        return [x ^ y for x, y in zip(t1, t2)]

    def validate_key(self, key):
        if len(key) < 8:
            raise ValueError("Key should be 8 bytes long")
        elif len(key) > 8:
            return key[:8]
        else:
            return key

    def generatekeys(self):  # Генерация всех ключей
        self.keys = []
        key = string_to_bit_array(self.password)
        key = self.permut(key, CP_1)  # Начальная перестановка ключа
        g, d = nsplit(key, 28)  # Разделение на (g->LEFT), (d->RIGHT)
        for i in range(16):  # 16 раундов
            g, d = self.shift(g, d, SHIFT[i])  # Применение сдвига, соответствующего раунду (не всегда 1)
            tmp = g + d  # Объединение
            self.keys.append(self.permut(tmp, CP_2))  # Получение Ki

    def shift(self, g, d, n):  # Сдвиг списка на заданное значение
        return g[n:] + g[:n], d[n:] + d[:n]

    def addPadding(self):  # Добавление дополнения к данным в соответствии с PKCS5
        pad_len = 8 - (len(self.text) % 8)
        self.text += pad_len * chr(pad_len)

    def removePadding(self, data):  # Удаление дополнения (предполагается, что оно есть)
        pad_len = ord(data[-1])
        return data[:-pad_len]

    def encrypt(self, key, text, padding=False):
        return self.run(key, text, ENCRYPT, padding)

    def decrypt(self, key, text, padding=False):
        return self.run(key, text, DECRYPT, padding)


if __name__ == '__main__':
    key = "secret_k"
    text = "Cute cat"
    d = Des()
    r = d.encrypt(key, text)
    r2 = d.decrypt(key, r)
    print("Encrypted:", r)
    print("Decrypted:", r2)
