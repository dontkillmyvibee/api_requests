import platform
import sys

from config import settings


def create_allure_environment_file():
    """
    Создаёт файл environment.properties для Allure с информацией
    о настройках проекта, операционной системе и версии Python.
    """
    items = [f'{key}={value}' for key, value in settings.model_dump().items()]

    os_info = f'{platform.system()}, {platform.release()}'
    items.append(f'os_info={os_info}')

    python_version = ' '.join(sys.version.split())
    items.append(f'python_version={python_version}')

    properties = '\n'.join(items)

    with open(settings.allure_results_dir.joinpath('environment.properties'), "w+", encoding="utf-8") as file:
        file.write(properties)
