import pyautogui as py
from time import sleep

def wait_until_locate_on_screen(path_to_image,
                                timeout=.1,
                                _grayscale=True,
                                _confidence=.5):
    while 1:
        image_pos = py.locateCenterOnScreen(path_to_image,
                                            grayscale=_grayscale,
                                            confidence=_confidence)
        if image_pos:
            return image_pos
        else:
            sleep(timeout)


def continue_if_not_locate_on_screen(path_to_image,
                                  timeout=.1,
                                  _grayscale=True,
                                  _confidence=.5):
    while 1:
        if py.locateCenterOnScreen(path_to_image,
                                   grayscale=_grayscale,
                                   confidence=_confidence):
            sleep(timeout)
        else:
            return


# def wait_until_locate(path_to_image,
#                       timeout=.1,
#                       _grayscale=True,
#                       _confidence=.5):
#     def inner(func):
#         while 1:
#             image_pos = py.locateCenterOnScreen(path_to_image,
#                                                 grayscale=_grayscale,
#                                                 confidence=_confidence)
#             if image_pos:
#                 return func(image_pos)
#             else:
#                 sleep(timeout)

#     return inner


def find_images(*images_pathes, timeout=.1, _grayscale=True, _confidence=.5):
    result = []
    for image in images_pathes:
        result.append(
            py.locateCenterOnScreen(image,
                                    grayscale=_grayscale,
                                    confidence=_confidence))
    return result


def find(path_to_image, timeout=.1, _grayscale=True, _confidence=.5):
    return py.locateCenterOnScreen(path_to_image,
                                   grayscale=_grayscale,
                                   confidence=_confidence)


def on_screen(path_to_image, timeout=.1, _grayscale=True, _confidence=.5) -> bool:
    if py.locateCenterOnScreen(path_to_image,
                               grayscale=_grayscale,
                               confidence=_confidence):
        return True
    else:
        return False

