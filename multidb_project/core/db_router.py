class CoreDatabaseRouter:
    """
    - Tablas de Django (auth/admin/sessions/etc) -> SOLO Postgres (default)
    - core.Client   -> Postgres (default)
    - core.Contract -> MySQL (mysql)
    """

    postgres_models = {"client"}
    mysql_models = {"contract"}

    django_apps = {
        "admin",
        "auth",
        "contenttypes",
        "sessions",
        "messages",
        "staticfiles",
    }

    def db_for_read(self, model, **hints):
        # Si quieres, puedes también rutear por app_label, pero tu enfoque por model_name está ok.
        if model._meta.app_label in self.django_apps:
            return "default"

        if model._meta.app_label == "core":
            if model._meta.model_name in self.postgres_models:
                return "default"
            if model._meta.model_name in self.mysql_models:
                return "mysql"

        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.django_apps:
            return "default"

        if model._meta.app_label == "core":
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
        # 1) Apps internas Django: SOLO Postgres
        if app_label in self.django_apps:
            return db == "default"

        # 2) App core: separar por modelo
        if app_label == "core":
            if model_name in self.postgres_models:
                return db == "default"
            if model_name in self.mysql_models:
                return db == "mysql"
            # si agregas más modelos a core, decide aquí (por defecto Postgres o bloquear)
            return db == "default"

        # 3) Otras apps (si existen): por defecto a Postgres
        return db == "default"
