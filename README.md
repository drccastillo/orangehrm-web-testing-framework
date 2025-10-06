# OrangeHRM Web Testing Automation Framework

Framework de automatización de pruebas web para OrangeHRM usando Python, Pytest, Selenium y Docker.

## 🏗️ Arquitectura y Patrones de Diseño

### Patrones Implementados:
- **Page Object Model (POM)**: Encapsulación de elementos y acciones de cada página
- **Base Page Pattern**: Clase base con métodos reutilizables para todas las páginas
- **Factory Pattern**: Configuración dinámica de navegadores
- **Singleton Pattern**: Gestión centralizada de configuración
- **Method Chaining**: Interfaz fluida para acciones en páginas

### Estructura del Proyecto:
```
web-testing-framework/
├── src/
│   ├── config/
│   │   ├── __init__.py
│   │   └── config.py              # Configuración centralizada
│   └── pages/
│       ├── __init__.py
│       ├── base_page.py           # Clase base con métodos comunes
│       └── login_page.py          # Page Object Model para login
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # Fixtures y configuración de pytest
│   └── test_login.py              # Tests de login
├── utils/
│   └── __init__.py
├── reports/                        # Reportes HTML y screenshots
├── .env                            # Variables de entorno
├── .gitignore
├── docker-compose.yml             # Selenium Grid con Chrome, Firefox, Edge
├── pyproject.toml                 # Dependencias y configuración (uv)
└── README.md
```

## 🚀 Configuración Inicial

### Prerequisitos:
- Python 3.10+
- Docker y Docker Compose
- UV package manager

### Instalación:

1. **Instalar UV** (si no lo tienes):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. **Instalar dependencias**:
```bash
uv sync
```

3. **Configurar variables de entorno**:
El archivo `.env` ya contiene:
```env
URL=http://localhost:8080/web/index.php
USER=******
PASSWORD=********
```

4. **Iniciar Selenium Grid**:
```bash
docker-compose up -d
```

Verificar que el grid está corriendo:
- Hub: http://localhost:4444
- Grid Console: http://localhost:4444/ui

## 🧪 Ejecutar Tests

### Ejecutar todos los tests:
```bash
uv run pytest
```

### Ejecutar tests específicos:
```bash
# Solo tests de login
uv run pytest tests/test_login.py

# Tests con marker 'smoke'
uv run pytest -m smoke

# Tests con marker 'login'
uv run pytest -m login

# Tests de regresión
uv run pytest -m regression
```

### Ejecutar en diferentes navegadores:
```bash
# Chrome (default)
uv run pytest --browser=chrome

# Firefox
uv run pytest --browser=firefox

# Edge
uv run pytest --browser=edge
```

### Ejecutar en modo headless:
```bash
uv run pytest --headless
```

### Ejecutar tests en paralelo:
```bash
uv run pytest -n auto
```

### Generar reporte HTML:
```bash
uv run pytest --html=reports/report.html --self-contained-html
```

## 📝 Escribir Nuevos Tests

### Ejemplo usando LoginPage:

```python
import pytest
from src.config.config import Config
from src.pages.login_page import LoginPage

@pytest.mark.smoke
def test_my_login(login_page: LoginPage):
    # El fixture 'login_page' ya navega a la página

    # Opción 1: Método directo
    login_page.login(Config.USERNAME, Config.PASSWORD)

    # Opción 2: Method chaining
    login_page.enter_username(Config.USERNAME)\
              .enter_password(Config.PASSWORD)
    login_page.click_login_button()

    # Verificaciones
    assert "dashboard" in login_page.get_current_url()
```

### Crear un Nuevo Page Object:

```python
from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage

class DashboardPage(BasePage):
    # Locators
    WELCOME_TEXT = (By.CSS_SELECTOR, ".oxd-topbar-header-breadcrumb")

    def __init__(self, driver, timeout=10):
        super().__init__(driver, timeout)

    def get_welcome_message(self):
        return self.get_text(self.WELCOME_TEXT)
```

## 🔧 Configuración Avanzada

### Variables de Entorno Disponibles (.env):
```env
# Application
URL=http://localhost:8080/web/index.php
USER=********
PASSWORD=*******

# Selenium Grid
SELENIUM_GRID_URL=http://localhost:4444

# Browser
BROWSER=chrome
HEADLESS=False

# Timeouts
DEFAULT_TIMEOUT=10
PAGE_LOAD_TIMEOUT=30
IMPLICIT_WAIT=5

# Window
WINDOW_WIDTH=1920
WINDOW_HEIGHT=1080
MAXIMIZE_WINDOW=True

# Screenshots
SCREENSHOT_ON_FAILURE=True
```

## 🎯 Características del Framework

### Base Page (base_page.py):
- ✅ Esperas explícitas automáticas
- ✅ Métodos reutilizables (click, send_keys, get_text, etc.)
- ✅ Manejo de frames
- ✅ Ejecución de JavaScript
- ✅ Scroll a elementos
- ✅ Verificación de visibilidad y presencia
- ✅ Logging integrado en todas las acciones

### Login Page (login_page.py):
- ✅ Locators centralizados
- ✅ Métodos de alto nivel (login, enter_username, etc.)
- ✅ Method chaining
- ✅ Validaciones específicas de la página
- ✅ Logging de acciones de login

### Fixtures (conftest.py):
- ✅ `driver`: WebDriver configurado y conectado al Grid
- ✅ `login_page`: LoginPage con navegación automática
- ✅ Screenshots automáticos en fallos
- ✅ Configuración de navegadores desde CLI
- ✅ Logging del ciclo de vida del WebDriver

### Logger Utility (utils/logger.py):
- ✅ Logger centralizado con configuración automática
- ✅ Logs a consola (INFO y superiores)
- ✅ Logs a archivo (DEBUG y superiores)
- ✅ Archivos de log diarios en `logs/` (raíz del proyecto)
- ✅ Decoradores `@log_test_step` y `@log_action`
- ✅ Mixin `LoggerMixin` para agregar logging a cualquier clase

### Custom Exceptions (utils/exceptions.py):
- ✅ Jerarquía de excepciones personalizada
- ✅ `FrameworkException`: Excepción base
- ✅ `ElementNotFoundException`: Elemento no encontrado
- ✅ `ElementNotClickableException`: Elemento no clickeable
- ✅ `InvalidParameterException`: Parámetro inválido
- ✅ `PageNotLoadedException`: Página no cargada
- ✅ `ConfigurationException`: Error de configuración

### Locators (src/pages/locators/):
- ✅ Locators centralizados en archivos separados
- ✅ Mantenimiento más fácil
- ✅ Reutilización entre tests
- ✅ Separación de responsabilidades

### Markers de Pytest:
- `@pytest.mark.smoke`: Tests rápidos de humo
- `@pytest.mark.regression`: Tests completos de regresión
- `@pytest.mark.login`: Tests específicos de login

## 📊 Reportes y Logs

Los reportes se generan automáticamente en:
- **HTML Report**: `reports/report.html`
- **Screenshots**: `reports/screenshots/` (solo en fallos)
- **Logs**: `logs/test_automation_YYYYMMDD.log` (logs diarios en raíz)

## 🧪 Unit Tests

El proyecto incluye unit tests para validar componentes del framework sin necesidad de navegador:

```bash
# Ejecutar todos los unit tests
uv run pytest unittests/ -v

# Ejecutar tests de un módulo específico
uv run pytest unittests/test_config.py -v
uv run pytest unittests/test_logger.py -v
uv run pytest unittests/test_exceptions.py -v
uv run pytest unittests/test_locators.py -v
```

### Unit Tests Disponibles:
- **test_config.py**: Tests de configuración y variables de entorno
- **test_logger.py**: Tests del sistema de logging
- **test_exceptions.py**: Tests de excepciones personalizadas
- **test_locators.py**: Tests de locators de páginas

## 🐳 Docker Compose

El `docker-compose.yml` incluye:
- Selenium Hub (puerto 4444)
- Chrome Node (VNC: 5900)
- Firefox Node (VNC: 5901)
- Edge Node (VNC: 5902)

### Comandos útiles:
```bash
# Iniciar grid
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener grid
docker-compose down

# Escalar nodos
docker-compose up -d --scale chrome=3
```

## 🔍 Debugging

### Ver sesiones del navegador con VNC:
```bash
# Instalar VNC viewer, luego conectar a:
# Chrome: localhost:5900
# Firefox: localhost:5901
# Edge: localhost:5902
# Password: secret (default)
```

### Ver logs en tiempo real:
```bash
# Ver logs del día actual
tail -f reports/logs/test_automation_$(date +%Y%m%d).log

# Ver logs con filtro
grep "ERROR" reports/logs/test_automation_*.log
grep "LoginPage" reports/logs/test_automation_*.log
```

## 📝 Uso del Logger

### En Page Objects:
```python
from utils.logger import TestLogger

class MyPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # El logger ya está disponible vía self.logger desde BasePage

    def my_action(self):
        self.logger.info("Executing my action")
        # ... código ...
```

### En Tests:
```python
from utils.logger import TestLogger, log_test_step

logger = TestLogger.get_logger(__name__)

@log_test_step("Verify user can login")
def test_login(login_page):
    logger.info("Starting login test")
    # ... código del test ...
```

### Usar LoggerMixin:
```python
from utils.logger import LoggerMixin

class MyHelper(LoggerMixin):
    def do_something(self):
        self.logger.info("Doing something")
        # ... código ...
```

### Niveles de Log:
- **DEBUG**: Información detallada para debugging (solo en archivo)
- **INFO**: Confirmación de que las cosas funcionan (consola y archivo)
- **WARNING**: Indicación de algo inesperado
- **ERROR**: Error que no detiene la ejecución
- **CRITICAL**: Error grave que puede detener el programa

## 📚 Referencia

Framework basado en principios de: https://github.com/taquimon/webauto2025

## 🤝 Contribuir

1. Seguir el patrón Page Object Model
2. Usar la clase BasePage para nuevas páginas
3. Agregar tests con markers apropiados
4. Documentar métodos públicos
5. Ejecutar tests antes de commit

## 📄 Licencia

MIT
