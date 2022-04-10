from functools import lru_cache

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from pydantic import BaseSettings

class Settings( BaseSettings ):
	counter: str = None

@lru_cache(1)
def get_settings():
	return Settings()

app = FastAPI()

@app.get( "/" )
def index( response_class: HTMLResponse ):
	with open( "index.html" ) as f:
		return HTMLResponse( f.read() )

@app.get( "/start" )
def start_counter():
	settings = get_settings()

	if settings.counter is not None and settings.counter.is_alive():
		return { "message": "Already started." }

	from death_counter import main
	from threading import Thread

	counter = Thread( target = main )
	counter.start()

	settings.counter = counter

	return { "message": "Ok" }

@app.get( "/counter" )
def get_counter():
	settings = get_settings()

	if settings.counter is None or not settings.counter.is_alive():
		return { "message": "Not started." }

	return { "message": "Running..." }

@app.get( "/stop" )
def stop_counter():
	from death_counter import stop

	settings = get_settings()

	if settings.counter is None or not settings.counter.is_alive():
		return { "message": "Not started." }

	stop()
	return { "message": "Stopped" }

@app.get( "/status" )
def get_status():
	from death_counter import load_config
	return load_config()
