import asyncio
import random
from app.parser.arbitr_parser import ArbitrParser
from app.services.excel_reader import read_cases
from app.db.crud import save_result
from app.utils.logger import logger
import os

CONCURRENCY = int(os.getenv("CONCURRENCY", 5))


async def worker(queue):
    parser = ArbitrParser()

    while True:
        case_number = await queue.get()

        try:
            result = await parser.parse_case(case_number)

            if "error" not in result:
                save_result(result)

            logger.info(f"Processed {case_number}")

        except Exception as e:
            logger.error(f"Error {case_number}: {e}")

        finally:
            queue.task_done()
            await asyncio.sleep(1 + random.random())


async def main():
    cases = read_cases("data/input.xlsx")

    queue = asyncio.Queue()

    for case in cases:
        queue.put_nowait(case)

    tasks = [
        asyncio.create_task(worker(queue))
        for _ in range(CONCURRENCY)
    ]

    await queue.join()

    for task in tasks:
        task.cancel()


if __name__ == "__main__":
    asyncio.run(main())
