from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Data model
class JobApplication(BaseModel):
    id: int | None = None
    company: str
    role: str
    status: str

applications = []
id_counter = 1

# GET all applications
@app.get("/applications")
def get_applications():
    return applications

# POST new application
@app.post("/applications", status_code=201)
def create_application(app_data: JobApplication):
    global id_counter
    app_data.id = id_counter
    id_counter += 1
    applications.append(app_data.dict())
    return app_data

# GET one application
@app.get("/applications/{app_id}")
def get_application(app_id: int):
    for app_item in applications:
        if app_item["id"] == app_id:
            return app_item
    raise HTTPException(status_code=404, detail="Application not found")

# PUT update application
@app.put("/applications/{app_id}")
def update_application(app_id: int, updated: JobApplication):
    for app_item in applications:
        if app_item["id"] == app_id:
            app_item["company"] = updated.company
            app_item["role"] = updated.role
            app_item["status"] = updated.status
            return app_item
    raise HTTPException(status_code=404, detail="Application not found")

# PATCH update status only
@app.patch("/applications/{app_id}")
def patch_application(app_id: int, status: str):
    for app_item in applications:
        if app_item["id"] == app_id:
            app_item["status"] = status
            return app_item
    raise HTTPException(status_code=404, detail="Application not found")

# DELETE application
@app.delete("/applications/{app_id}", status_code=204)
def delete_application(app_id: int):
    global applications
    applications = [app_item for app_item in applications if app_item["id"] != app_id]
    return
