# Create Rocketry app
import asyncio
from rocketry import Rocketry
from rocketry.conds import every
app = Rocketry(execution="async")


# Create some tasks

@app.task('every 5 seconds')
async def do_things():
    print('hello')
    "This runs for short time"
    await asyncio.sleep(1)

if __name__ == "__main__":
    app.run()