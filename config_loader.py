import yaml


class ConfigLoader:
    def __init__(self, file_path):
        self.config = self.read_yaml_to_dict(file_path)

    def read_yaml_to_dict(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
            return data
        except FileNotFoundError:
            print(f"Файл {file_path} не найден.")
        except yaml.YAMLError as exc:
            print(f"Ошибка при чтении YAML файла: {exc}")

    def get_config(self):
        return self.config
