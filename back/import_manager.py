import asyncio
from importlib import import_module


def import_modules(modules_list):

    modules_path_list = [f"modules.{module_name}.main" for module_name in modules_list]

    imported_modules = []

    for module in modules_path_list:
        imported_modules.append(import_module(module))

    return imported_modules


def start_modules(imported_modules, SCRIPT_PATH):
    modules_init_event_loop = asyncio.new_event_loop()
    tasks = []
    for module in imported_modules:
        tasks.append(
            modules_init_event_loop.create_task(
                module.module_start(SCRIPT_PATH=SCRIPT_PATH)
            )
        )

    wait_tasks = asyncio.wait(tasks)

    modules_init_event_loop.run_until_complete(wait_tasks)
    modules_init_event_loop.close()


def execute_modules(imported_modules, SCRIPT_PATH, event, VK_TOKEN):
    modules_execute_event_loop = asyncio.new_event_loop()
    tasks = []
    for module in imported_modules:
        tasks.append(
            modules_execute_event_loop.create_task(
                module.module_execute(
                    SCRIPT_PATH=SCRIPT_PATH,
                    event=event,
                    VK_TOKEN=VK_TOKEN,
                )
            )
        )

    wait_tasks = asyncio.wait(tasks)

    modules_execute_event_loop.run_until_complete(wait_tasks)
    modules_execute_event_loop.close()
