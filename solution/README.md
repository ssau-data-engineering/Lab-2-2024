# Engineering

## Ионов Артем группа 6231-010402D

### Лабораторная работа №1 "Базовый пайплайн работы с данными"

# Необходимый минимум для выполнения лабораторных работ:

Что было выполнено для начала:

1. Для начала был установлен клиент программы Docker Desktop по [ссылке](https://www.docker.com/products/docker-desktop/). Проведена настройка для запуска докера.
   
 ```
$ dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
 ```

 ```
$ dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
 ```
2. Для работы был выбран [VS Code](https://code.visualstudio.com/insiders/). Затем была проведена настройка, установка требуемых расширений для работы:

   * [ms-python.python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
   * [ms-toolsai.jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter)
   * [ms-vscode-remote.vscode-remote-extensionpack](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)
   * [ms-azuretools.vscode-docker](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)

3. Клонирование репозитория. Склонировал себе [репозиторий](https://github.com/ssau-data-engineering/Prerequisites.git ) в заранее созданную папку GitHere.

 ```
git clone https://github.com/ssau-data-engineering/Prerequisites.git 
 ```
4. Далее, перед запуском контейнеров, была выполнена последовательнось команд:


```bash
    docker network create data-engineering-labs-network
```

Подготавливка к запуску **Apache airflow**

```bash
    docker compose -f docker-compose.airflow.yaml up airflow-init
```

Для запуска, `airflow` `nifi` `elasticsearch` `posgresql` `mlflow` использовались следующие, соответственно, команды.

```bash
    docker compose -f docker-compose.airflow.yaml up --build -d
```    
    
```bash
    docker compose -f docker-compose.nifi.yaml up --build -d
```    
    
```bash
    docker compose -f docker-compose.elasticsearch.yaml up --build -d
```    
    
```bash
    docker compose -f docker-compose.postgresql.yaml up --build -d
```

```bash
    docker compose -f docker-compose.mlflow.yaml up --build -d
```

5. Запущенные контейнеры в Docker

![image](https://github.com/user-attachments/assets/41eaed57-c69b-4a4a-aa2f-3ba4910b417f)

### Лабораторная работа №1 "Базовый пайплайн работы с данными"

Используя DAG нужно реализовать пайплайн обработки данных, в файлах csv. Схема пайплайна:

![image](https://github.com/user-attachments/assets/f26f7781-7067-4e42-af33-2c73395d01ef)



