import importlib
import os
import sys

from application.models.db.company_model import Base
from application.models.db.connection import engine
from application.routes import app

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    importlib.import_module("migration")

    os.environ["PYTHON_ENV"] = "PRODUCTION"
    sys.path.insert(0, "application")
    app.run(host="0.0.0.0", port=8000)
