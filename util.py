import copy
import cv2
import numpy as np

# Глобальные переменные для хранения состояния рисования
drawingWhite = False  # Флаг для проверки, происходит ли рисование
drawingBlack = False
canvas_size = (8, 8)  # Размер холста в пикселях
scale_factor = 50  # Масштаб для отображения большого окна

# Создаем черный холст размером 8x8 пикселей
image = np.zeros((canvas_size[0], canvas_size[1], 3), dtype=np.uint8)


def get_map(for_item=False):
    global drawingWhite, drawingBlack, image, scale_factor

    # Функция-обработчик событий мыши
    def draw(event, x, y, flags, param):
        global drawingWhite, drawingBlack, image, scale_factor

        # Преобразуем координаты из окна в координаты холста
        canvas_x, canvas_y = x // scale_factor, y // scale_factor

        if event == cv2.EVENT_LBUTTONDOWN:  # Начало рисования
            drawingWhite = True
            cv2.rectangle(image, (canvas_x, canvas_y), (canvas_x, canvas_y), (255, 255, 255), -1)

        if event == cv2.EVENT_RBUTTONDOWN and not drawingWhite:  # Начало рисования
            drawingBlack = True
            cv2.rectangle(image, (canvas_x, canvas_y), (canvas_x, canvas_y), (0, 0, 0), -1)

        elif event == cv2.EVENT_MOUSEMOVE:  # Рисование при перемещении мыши
            if drawingWhite:
                cv2.rectangle(image, (canvas_x, canvas_y), (canvas_x, canvas_y), (255, 255, 255), -1)
            elif drawingBlack:
                cv2.rectangle(image, (canvas_x, canvas_y), (canvas_x, canvas_y), (0, 0, 0), -1)

        elif event == cv2.EVENT_LBUTTONUP:  # Завершение рисования
            drawingWhite = False

        elif event == cv2.EVENT_RBUTTONUP:  # Завершение рисования
            drawingBlack = False

    # Инициализация окна и привязка обработчика событий
    cv2.namedWindow("Drawing App")
    cv2.setMouseCallback("Drawing App", draw)

    # Основной цикл программы
    while True:
        # Масштабируем изображение для отображения
        display_image = cv2.resize(image, (canvas_size[1] * scale_factor, canvas_size[0] * scale_factor),
                                   interpolation=cv2.INTER_NEAREST)
        cv2.imshow("Drawing App", display_image)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):  # Выход из программы
            break
        elif key == ord("e"):  # Очистка холста
            image = np.zeros((canvas_size[0], canvas_size[1], 3), dtype=np.uint8)

    cv2.destroyAllWindows()

    if image.sum() == 0:
        return 0

    array = []
    for y in range(image.shape[0]):
        help_array = []
        for x in range(image.shape[1]):
            if image[y][x][0] == 255:
                if for_item:
                    help_array.append(4)
                else:
                    help_array.append(1)
            else:
                help_array.append(0)
        array.append(help_array)

    image = np.zeros((canvas_size[0], canvas_size[1], 3), dtype=np.uint8)

    return array

def draw_images(_images):
    scale_factor = 50  # Размер одной ячейки в пикселях

    for idx, matrix in enumerate(_images):
        size = len(matrix)  # Размер матрицы (предполагается квадратная)
        image_size = size * scale_factor

        # Создаем черное изображение
        image = np.zeros((image_size, image_size, 3), dtype=np.uint8)

        # Цвета для значений
        colors = {
            4: (0, 0, 255),  # Красный
            1: (255, 255, 255),  # Белый
            0: (0, 0, 0)  # Черный
        }

        # Рисуем матрицу
        for i in range(size):
            for j in range(size):
                value = matrix[i][j]
                color = colors.get(value, (0, 0, 0))  # По умолчанию черный
                x1, y1 = j * scale_factor, i * scale_factor
                x2, y2 = x1 + scale_factor, y1 + scale_factor
                cv2.rectangle(image, (x1, y1), (x2, y2), color, -1)

        # Отображаем каждую матрицу в отдельном окне
        window_name = f"Matrix {idx + 1}"
        cv2.imshow(window_name, image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def block_bast_items_transformation(block_bast_items):
    for i, block_bast_item in enumerate(block_bast_items):
        min_x = 8
        min_y = 8
        max_x = -1
        max_y = -1

        for height in range(len(block_bast_item)):
            for width in range(len(block_bast_item[height])):
                if block_bast_item[height][width] == 4:
                    if min_x > width:
                        min_x = width
                    if min_y > height:
                        min_y = height
                    if max_x < width:
                        max_x = width
                    if max_y < height:
                        max_y = height

        block_bast_item = cut_array(block_bast_item, min_x, max_x + 1, min_y, max_y + 1)

        block_bast_items[i] = block_bast_item


def cut_array(array, min_x, max_x, min_y, max_y):
    array = array[min_y:max_y]
    for _i in range(len(array)):
        array[_i] = array[_i][min_x:max_x]

    return array


def plus_array(first_array, second_array):
    array = copy.deepcopy(first_array)
    for y in range(len(array)):
        for x in range(len(array[y])):
            array[y][x] += second_array[y][x]

    return array


def paste_array(copy_array, paste_array, x_offset, y_offset):
    array = copy.deepcopy(paste_array)
    for y in range(y_offset, y_offset + len(copy_array)):
        for x in range(x_offset, x_offset + len(copy_array[y-y_offset])):
            array[y][x] = copy_array[y-y_offset][x-x_offset]

    return array


def clean_map(block_bast_map):
    array = copy.deepcopy(block_bast_map)
    for y in range(len(array)):
        for x in range(len(array[y])):
            if array[y][x] == 0:
                break
        else:
            array[y] = [3 for _ in range(len(array[y]))]

    for x in range(len(array[0])):
        for y in range(len(array)):
            if array[y][x] == 0:
                break
        else:
            for y in range(len(array)):
                array[y][x] = 3

    for y in range(len(array)):
        for x in range(len(array[y])):
            if array[y][x] == 3:
                array[y][x] = 0

    return array
