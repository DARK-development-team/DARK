import importlib
import importlib.util

bots = []  # dont touch :D
arenas = []  # dont touch :D
# ['archipelago','wasteland','dungeon','fisher_island']
profiling_metrics = []  # dont touch :D
# possible metrics ['all', 'total', 'avg']


def load_bot_class(bot_code_path, bot_class_name, i: int):
    spec = importlib.util.spec_from_file_location(f'module{i}', bot_code_path)
    bot_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bot_module)
    return getattr(bot_module, bot_class_name)


def prepare_config_controllers(bots):
    return [load_bot_class(bot_p, bot_cn, i)(f'{i}') for i, (bot_p, bot_cn) in enumerate(bots)]


CONFIGURATION = {
    'arenas': arenas,
    'controllers': prepare_config_controllers(bots),
    'start_balancing': False,
    'visualise': False,
    'show_sight': None,
    'runs_no': 300,
    'profiling_metrics': profiling_metrics,
}
