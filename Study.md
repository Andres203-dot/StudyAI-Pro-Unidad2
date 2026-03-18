# StudyAI Pro - Documentación Técnica

**StudyAI Pro** es una aplicación de escritorio creada para ayudar con el seguimiento y análisis de sesiones de estudio. Construida con Python y Tkinter, la cual nos ofrece una interfaz gráfica con estética moderna y persistencia de datos local segura.

---

##  Características Principales

### Sistema de Autenticación y Seguridad
*   **Gestión de Identidad:** Registro e inicio de sesión de usuarios.
*   **Seguridad:** Almacenamiento de contraseñas cifradas mediante algoritmo **MD5**.
*   **Privacidad:** Datos aislados por ID de usuario.

### Dashboard Interactivo
*   **KPIs en Tiempo Real:** Visualización inmediata de:
    *   Total de sesiones realizadas.
    *   Horas acumuladas de estudio.
    *   Promedio de rendimiento/puntuación.
*   **Interfaz:** Diseño limpio con tarjetas de información y consejos dinámicos.

### Gestión de Sesiones
*   **Registro Detallado:** Formulario para ingresar:
    *   Materia/Asignatura.
    *   Duración (minutos).
    *   Puntuación de autoevaluación (1-10).
*   **Persistencia:** Guardado automático en base de datos relacional.

### Análisis y Estadísticas
*   **Reportes Agregados:** Desglose por materia que incluye:
    *   Horas totales dedicadas por asignatura.
    *   Cantidad de sesiones.
    *   Promedio de calidad de estudio.

### Administración de Datos
*   **Reset Parcial:** Funcionalidad para limpiar el historial de sesiones manteniendo el usuario.
*   **Borrado Total:** Opción para eliminar permanentemente la cuenta y todos los registros asociados.

---

## Especificaciones Técnicas

### Stack Tecnológico
| Componente | Tecnología | Descripción |
|------------|------------|-------------|
| **Lenguaje** | Python 3.x | Lógica principal del backend y frontend. |
| **GUI** | Tkinter | Biblioteca gráfica nativa para la interfaz de usuario. |
| **Base de Datos** | SQLite3 | Motor de base de datos relacional ligero y sin servidor. |
| **Cifrado** | Hashlib | Biblioteca para hashing criptográfico (MD5). |

### Estructura de Base de Datos (`studyai.db`)

#### 1. Tabla `users`
Almacena las credenciales de acceso.
*   `id`: INTEGER PRIMARY KEY (Identificador único).
*   `username`: TEXT UNIQUE (Nombre de usuario).
*   `password`: TEXT (Hash MD5 de la contraseña).

#### 2. Tabla `sessions`
Registra cada sesión de estudio vinculada a un usuario.
*   `id`: INTEGER PRIMARY KEY.
*   `user_id`: INTEGER (Clave foránea hacia `users.id`).
*   `subject`: TEXT (Nombre de la materia).
*   `duration`: INTEGER (Tiempo en minutos).
*   `score`: INTEGER (Calificación 1-10).
*   `date`: TEXT (Fecha de registro YYYY-MM-DD).

---

## Instalación y Ejecución

1.  **Requisitos:** Tener instalado Python 3.x.
2.  **Ejecución:**
    ```bash
    python studyai_simple.py
    ```
3.  **Primer Uso:**
    *   Utilice el botón **"➕ REGISTRAR"** para crear una nueva cuenta.
    *   Acceda con sus credenciales para ver el Dashboard.
