# Пайплайн для инференса данных

- использованы кастомные образы, запушенные на хаб
- взаимодействие с моделью - через API HuggingFace, через ui получен токен
- url для преобразования аудио в текст: https://api-inference.huggingface.co/models/openai/whisper-small
- url для составления конспекта: https://api-inference.huggingface.co/models/slauw87/bart_summarisation

# Пайплайн для обучения модели

- выбран тестовый датасет для классификации https://www.kaggle.com/datasets/prishasawhney/mushroom-dataset
- read_data - преобразование данных в данные для обучения и тестирования
- train_model - построение простейшей модели
- использован кастомный образ