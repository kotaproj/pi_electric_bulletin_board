import asyncio
from typing import Optional
from pathlib import Path
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

from schemas import ItemReg, ItemShow, ItemDo
from utl import regist_job, show_job, do_job

app = FastAPI()


@app.post("/do")
async def do_item(  item: ItemDo,
                        background_tasks: BackgroundTasks = None):
    background_tasks.add_task(do_job, job_id=item.job_id, msg=item.message, color=item.color,\
                                    fontsize=item.fontsize, bright=item.bright, interval=item.interval
    )
    return item

@app.post("/regist")
async def regist_item(  item: ItemReg,
                        background_tasks: BackgroundTasks = None):
    background_tasks.add_task(regist_job, job_id=item.job_id, msg=item.message, color=item.color,\
                                        fontsize=item.fontsize
    )
    return item

@app.post("/show")
async def show_item(  item: ItemShow,
                        background_tasks: BackgroundTasks = None):
    background_tasks.add_task(show_job, job_id=item.job_id, bright=item.bright, interval=item.interval)
    return item

@app.get('/results')
async def results():
    p = Path('.')
    result_files = [str(pp).replace(".png", "") for pp in p.glob('*.png')]
    return result_files
