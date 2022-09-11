from fastapi import FastAPI
import uvicorn
import json
from business_object.feat_statistic import FeatStatistic


app = FastAPI()
feat_statistic = FeatStatistic()

@app.get("/feat-count")
async def feat_count():
    return json.loads(feat_statistic.feat_count())

@app.get("/feat-mean")
async def feat_mean():
    return json.loads(feat_statistic.feat_mean())


if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=5000)