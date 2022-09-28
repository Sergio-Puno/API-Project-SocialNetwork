from fastapi import FastAPI
from .routers import post, user, auth, vote

# Create our instance of FasAPI
app = FastAPI()


@app.get("/")
def root():
    """BASE DIRECTORY"""

    return {"message": "Hello World."}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)