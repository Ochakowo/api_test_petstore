# Выбираем на https://hub.docker.com/
FROM python:3.12-alpine

# Куда копировать (если нет папки, то будет создана. / - в корне)
WORKDIR /api-test_app

# Файл с зависимостями, куда копировать
COPY requirements.txt ./

# Запускаем для сборки контейнера с зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Параметры для запуска тестов при старте контейнера
ENTRYPOINT ["pytest", "-v", "--alluredir", "allure-results"]
# CMD подставится в конец ENTRYPOINT, если запустим контейнер без параметров (тест по дефолту). CMD заменяется внешним параметром.
CMD ["test_api.py"]

# Собираем образ: docker build -t api-test_app .

# Копируем тесты в образ в папку tests, указываем обсолютный путь откуда и куда через двоеточие (~ до директории с проектами, или /$(pwd) текущая папка с проектом) - (-v D:/Study/Python/exam:/api_test_app/tests)
# Запускаем контейнер (-rm - удалит после выполнения): docker run -it -v D:/Study/Python/exam:/api_test_app/tests api-test_app ./tests/test_api.py

# Запускаем контейнер с allur'ом на борту. Документация: https://github.com/fescobar/allure-docker-service-ui?tab=readme-ov-file#usage
# -v - сокращенный путь монтирования для --mount type=volume,source=allure_projects,target=/app/projects

# Будет запущено 2 сервиса: "frankescobar/allure-docker-service" и "frankescobar/allure-docker-service-ui":

# Первый сервис мониторит папку с репортами (CHECK_RESULTS_EVERY_SECONDS=NONE - если указать время в сек, будет проверять папку резалт через заданное время, KEEP_HISTORY=1 - сколько истории будет хранить):
# docker run -p 5050:5050 -e CHECK_RESULTS_EVERY_SECONDS=5 -e KEEP_HISTORY=3 --mount type=volume,source=allure_projects,target=/app/projects --mount type=volume,source=allure_report,target=/app/allure-report --mount type=volume,source=allure_results,target=/app/allure-results frankescobar/allure-docker-service
# Проверяем запуск сервиса: http://localhost:5050/

# Второй сервис непосредственно c allur'ом:
# docker run -p 5252:5252 -e ALLURE_DOCKER_PUBLIC_API_URL=http://localhost:5050 frankescobar/allure-docker-service-ui
# Проверяем запуск сервиса: http://localhost:5252/

# Перезапускаем контейнер с тестами, чтобы присоединить папку с результатами из volume:
# docker run -it -v D:/Study/Python/exam:/api_test_app/tests --mount type=volume,source=allure_results,target=/api_test_app/allure-results api-test_app ./tests/test_api.py
