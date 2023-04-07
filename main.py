from app.controller import AppMenu
import logging

if __name__ == "__main__":
    logging.basicConfig(filename="log.log",
                        format="%(asctime)s - %(levelname)s: %(lineno)d - %(message)s")
    try:
        AppMenu()
    except BaseException:
        logging.exception("An exception was thrown!")
        print("Произошла ошибка. Свяжитесь с автором для решения.\n"
              "Error was found. Please contact with Author.")
