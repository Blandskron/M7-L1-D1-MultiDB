class CoreDatabaseRouter:
    """
    Router multi-DB:
    - Client -> PostgreSQL (default)
    - Contract -> MySQL (mysql)
    """

    postgres_models = {"client"}
    mysql_models = {"contract"}

    def db_for_read(self, model, **hints):
        if model._meta.model_name in self.postgres_models:
            return "default"
        if model._meta.model_name in self.mysql_models:
            return "mysql"
        return None

    def db_for_write(self, model, **hints):
        if model._meta.model_name in self.postgres_models:
            return "default"
        if model._meta.model_name in self.mysql_models:
            return "mysql"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        db1 = self.db_for_read(obj1.__class__)
        db2 = self.db_for_read(obj2.__class__)
        if db1 and db2 and db1 != db2:
            return False
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label != "core":
            return None

        if model_name in self.postgres_models:
            return db == "default"

        if model_name in self.mysql_models:
            return db == "mysql"

        return None
