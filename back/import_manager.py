import asyncio
from datetime import datetime
from importlib import import_module


def import_modules(modules_list):
    # import all "main.py" files by template <SCRIPT_PATH>/modules/module_1/main.py
    modules_path_list = [f"modules.{module_name}.main" for module_name in modules_list]

    imported_modules = []
    for module in modules_path_list:
        imported_modules.append(import_module(module))

    return imported_modules


def start_modules(imported_modules, SCRIPT_PATH, print_messages=True, modules_list=[]):
    """
    executes "module_start()" function of each imported module in "imported_modules"
    "SCRIPT_PATH" param is just passing to the "module_start()" function
    """
    modules_init_event_loop = asyncio.new_event_loop()
    tasks = []
    for i, module in enumerate(imported_modules):
        tasks.append(
            modules_init_event_loop.create_task(
                module.module_start(SCRIPT_PATH=SCRIPT_PATH)
            )
        )
        if print_messages:

            APP_NAME = "import_manager"
            date = ".".join(
                str(el) for el in list(datetime.now().date().timetuple())[:3][::-1]
            )
            time = str(datetime.now().time()).split(".")[0]
            date = time + " " + date

            print(APP_NAME, f": Imported {modules_list[i]}")
            print()

    wait_tasks = asyncio.wait(tasks)

    modules_init_event_loop.run_until_complete(wait_tasks)
    modules_init_event_loop.close()


def execute_modules(imported_modules, SCRIPT_PATH, event, vk_session):
    """
    executes "module_execute()" function of each imported module in "imported_modules"
    modules should react on "event"
    "SCRIPT_PATH, vk_session" params are just passing to the "module_start()" function
    """
    modules_execute_event_loop = asyncio.new_event_loop()
    tasks = []
    for module in imported_modules:

        # preexecuting async function
        module_execution_task = module.module_execute(
            SCRIPT_PATH=SCRIPT_PATH,
            event=event,
            vk_session=vk_session,
        )

        tasks.append(modules_execute_event_loop.create_task(module_execution_task))

    wait_tasks = asyncio.wait(tasks)

    modules_execute_event_loop.run_until_complete(wait_tasks)
    modules_execute_event_loop.close()
