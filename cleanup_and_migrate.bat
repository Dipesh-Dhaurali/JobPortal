@echo off
REM Clear Python cache and run migrations
echo Cleaning Python cache files...
for /r . %%d in (__pycache__) do (
    if exist "%%d" (
        echo Removing %%d
        rmdir /s /q "%%d"
    )
)

echo Removing .pyc files...
for /r . %%f in (*.pyc) do (
    if exist "%%f" (
        del "%%f"
    )
)

echo.
echo Running Django makemigrations...
python manage.py makemigrations authuser
python manage.py makemigrations candidate
python manage.py makemigrations hr
python manage.py makemigrations admin_portal

echo.
echo Running Django migrate...
python manage.py migrate

echo.
echo Done! Your database is ready.
pause
