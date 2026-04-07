from playwright.async_api import async_playwright
from datetime import datetime


class ArbitrParser:
    async def parse_case(self, case_number: str) -> dict:
        """Парсинг одного дела"""

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            try:
                await page.goto("https://kad.arbitr.ru/")

                # Ввод номера дела
                await page.fill("input[type='text']", case_number)
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(3000)

                # Переход в дело
                await page.click(f"text={case_number}")
                await page.wait_for_timeout(3000)

                # Вкладка "Электронное дело"
                await page.click("text=Электронное дело")
                await page.wait_for_timeout(3000)

                # Получаем строки таблицы
                rows = await page.query_selector_all("table tr")

                if not rows:
                    return {"case_number": case_number, "error": "Нет данных"}

                last_row = rows[-1]

                cells = await last_row.query_selector_all("td")

                last_date = None
                document_name = None

                if len(cells) >= 2:
                    date_text = await cells[0].text_content()
                    document_name = await cells[1].text_content()

                    if date_text:
                        last_date = datetime.strptime(date_text.strip(), "%d.%m.%Y")

                return {
                    "case_number": case_number,
                    "last_date": last_date,
                    "document_name": document_name.strip() if document_name else None
                }

            except Exception as e:
                return {"case_number": case_number, "error": str(e)}

            finally:
                await browser.close()
