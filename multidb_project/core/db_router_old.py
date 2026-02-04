class CoreDatabaseRouter:
    """
    Router multi-DB para la app core.

    Reglas:
    - Client   -> PostgreSQL (alias: default)
    - Contract -> MySQL      (alias: mysql)

    Django invoca estos métodos para:
    - seleccionar DB en lecturas/escrituras
    - decidir si se permite una relación entre objetos
    - decidir en qué DB migrar cada modelo
    """

    postgres_models = {"client"}
    mysql_models = {"contract"}

    def db_for_read(self, model, **hints):
        """
        Selecciona la base de datos para operaciones de lectura (SELECT).
        """
        if model._meta.model_name in self.postgres_models:
            return "default"
        if model._meta.model_name in self.mysql_models:
            return "mysql"
        return None

    def db_for_write(self, model, **hints):
        """
        Selecciona la base de datos para operaciones de escritura (INSERT/UPDATE/DELETE).
        """
        if model._meta.model_name in self.postgres_models:
            return "default"
        if model._meta.model_name in self.mysql_models:
            return "mysql"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Bloquea relaciones ORM (FK/M2M) entre objetos que residan en DBs distintas.
        """
        db1 = self.db_for_read(obj1.__class__)
        db2 = self.db_for_read(obj2.__class__)
        if db1 and db2 and db1 != db2:
            return False
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Controla en qué base se ejecutan migraciones por modelo.
        """
        if app_label != "core":
            return None

        if model_name in self.postgres_models:
            return db == "default"

        if model_name in self.mysql_models:
            return db == "mysql"

        return None
