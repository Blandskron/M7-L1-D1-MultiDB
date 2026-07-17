# Guía del código educativo

El código ejecutable es la fuente de verdad y está organizado para seguir este recorrido:

1. `multidb_project/settings.py`: declara las conexiones `default` y `contracts`.
2. `core/models.py`: traduce entidades Python a tablas y define restricciones.
3. `core/migrations/0001_initial.py`: versión reproducible del esquema.
4. `core/db_router.py`: selecciona conexión para lectura, escritura y migración.
5. `core/queries.py`: compara filtros y agregaciones ORM con SQL crudo.
6. `core/forms.py` y `core/views.py`: validan, escriben y muestran datos.
7. `core/admin.py`: gestión desde el panel de Django.
8. `core/tests.py`: demuestra que ambas bases, API, formularios, SQL y ORM funcionan.

La explicación conceptual, motores soportados y drivers de instalación están en el `README.md` de la raíz.
