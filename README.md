# Sistema de Gestión de Clientes y Contratos Multi-Base de Datos (Django)

## 📌 Descripción general

Este proyecto es una aplicación desarrollada con **Django** que demuestra de forma práctica y estructurada la **integración del framework con múltiples motores de bases de datos relacionales**, utilizando el **ORM de Django**, migraciones controladas y consultas avanzadas.

El sistema permite administrar **clientes** y **contratos**, almacenando cada entidad en una **base de datos distinta**, resolviendo uno de los escenarios más complejos y reales del acceso a datos empresarial: **arquitecturas Multi-DB**.

---

## 🎯 Objetivos del proyecto

* Comprender cómo Django se integra con bases de datos relacionales
* Aplicar el ORM de Django para definir modelos, consultas y agregaciones
* Configurar y utilizar **múltiples bases de datos simultáneamente**
* Controlar migraciones por base de datos usando **Database Routers**
* Comparar consultas ORM con SQL crudo
* Implementar una API simple que exponga datos combinados desde distintas DB

---

## 🧱 Arquitectura general

### Bases de datos utilizadas

| Base de datos | Motor      | Alias Django | Modelo almacenado |
| ------------- | ---------- | ------------ | ----------------- |
| Clientes      | PostgreSQL | `default`    | `Client`          |
| Contratos     | MySQL      | `mysql`      | `Contract`        |

Cada base de datos es **independiente**, no existe una ForeignKey real entre tablas, lo que obliga a resolver la relación a nivel de aplicación, como ocurre en sistemas distribuidos reales.

---

## 🗂️ Estructura del proyecto

```
multidb_project/
├── multidb_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── core/
│   ├── admin.py
│   ├── models.py
│   ├── db_router.py
│   ├── queries.py
│   ├── views.py
│   └── urls.py
│
├── code.md
├── command.md
└── requirements.txt
```

---

## 🧠 Modelado de datos

### Client (PostgreSQL)

* Identifica a los clientes del sistema
* Almacenado exclusivamente en PostgreSQL
* Campos principales:

  * nombre
  * email (único)
  * país
  * estado activo
  * fecha de creación

### Contract (MySQL)

* Representa contratos asociados a clientes
* Almacenado exclusivamente en MySQL
* Relación con cliente mediante `client_id` (sin FK real)
* Campos principales:

  * client_id
  * título
  * monto
  * fecha de firma
  * estado activo

---

## 🔀 Enrutamiento Multi-DB

El proyecto utiliza un **Database Router personalizado** (`CoreDatabaseRouter`) que define:

* En qué base se leen los modelos
* En qué base se escriben
* En qué base se ejecutan las migraciones
* Bloqueo de relaciones ORM entre DBs distintas

Esto permite que Django:

* Migre `Client` solo en PostgreSQL
* Migre `Contract` solo en MySQL
* Use el ORM sin ambigüedades

---

## 🔍 Acceso a datos y consultas

### ORM (por base de datos)

* Filtros simples (`filter`)
* Agregaciones (`Count`, `Sum`)
* Consultas agrupadas (`annotate`)
* Uso explícito de `.using("default")` y `.using("mysql")`

### Combinación de datos Multi-DB

Dado que Django **no permite JOINs entre bases distintas**, el proyecto implementa:

1. Consultas agregadas en MySQL (`Contract`)
2. Consultas base en PostgreSQL (`Client`)
3. Unión de resultados en memoria (Python)

Este enfoque es **correcto, seguro y realista** para arquitecturas empresariales.

---

## 🌐 API expuesta

La aplicación expone endpoints REST simples usando vistas funcionales:

| Endpoint                | Descripción                        |
| ----------------------- | ---------------------------------- |
| `/api/clients/`         | Lista de clientes activos          |
| `/api/clients/stats/`   | Total de contratos por cliente     |
| `/api/clients/amounts/` | Monto total contratado por cliente |

Las respuestas combinan información proveniente de **PostgreSQL y MySQL**.

---

## 🛠️ Paquetes utilizados

* `Django`
* `psycopg2-binary` (driver PostgreSQL)
* `mysqlclient` (driver MySQL)

Todos los paquetes están declarados en `requirements.txt`.

---

## 📄 Documentación incluida

* **`code.md`**
  Contiene **todo el código fuente relevante**, limpio y listo para copiar/pegar, sin comandos.

* **`command.md`**
  Contiene **todos los comandos ejecutados** durante la creación y despliegue del proyecto.
