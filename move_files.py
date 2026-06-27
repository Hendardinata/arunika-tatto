import shutil
import os

# Create frontend dir if not exists
os.makedirs("frontend", exist_ok=True)

# Move templates
if os.path.exists("app/templates"):
    shutil.move("app/templates", "frontend/templates")

# Move static
if os.path.exists("app/static"):
    shutil.move("app/static", "frontend/static")

# Create missing backend dirs
dirs = [
    "backend/app/controllers",
    "backend/app/exceptions",
    "backend/app/extensions",
    "backend/app/logs",
    "backend/app/middlewares",
    "backend/app/models",
    "backend/app/repositories",
    "backend/app/routes",
    "backend/app/schemas",
    "backend/app/security",
    "backend/app/services",
    "backend/app/utils"
]
for d in dirs:
    os.makedirs(d, exist_ok=True)

print("Moved templates/static and created directories.")
