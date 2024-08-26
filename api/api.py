from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .routers import cattles, user, farms, calves, annotations, vaccines, data_analysis

app = FastAPI()

app.include_router(user.router)
app.include_router(farms.router)
app.include_router(cattles.router)
app.include_router(calves.router) 
app.include_router(annotations.router)
app.include_router(vaccines.router)
app.include_router(data_analysis.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return

@app.post("/post")
async def post_testing(request: Request):
    post = await request.json()
    return post