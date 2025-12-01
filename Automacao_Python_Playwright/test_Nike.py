import asyncio
import pandas as pd
from playwright.async_api import Playwright, async_playwright

async def scrape_shoes(playwright: Playwright, url: str) -> None:
    browser = await playwright.chromium.launch(headless=False)
    page = await browser.new_page(viewport={"width": 1920, "height": 1080})

    await page.goto(url)

    lista_tenis = []

    container_tenis = await page.query_selector_all(".product-card")

    for tenis in container_tenis:
        nome_tenis = await tenis.query_selector(".product-card__title")
        nome_tenis = await nome_tenis.text_content() if nome_tenis else "N/A"

        preco_tenis = await tenis.query_selector(".product-price")
        preco_tenis = await preco_tenis.text_content() if preco_tenis else "N/A"

        cor_tenis = await tenis.query_selector(".product-card__product-count")
        cor_tenis = await cor_tenis.text_content() if cor_tenis else "N/A"

        status_tenis = await tenis.query_selector(".product-card__messaging")
        status_tenis = await status_tenis.text_content() if status_tenis else "N/A"

        link_tenis = await tenis.query_selector(".product-card__link-overlay")
        link_tenis = await link_tenis.get_attribute("href") if link_tenis else "N/A"

        shoe_info = {
            "nome": nome_tenis,
            "preco": preco_tenis,
            "cor": cor_tenis,
            "status": status_tenis,
            "link": link_tenis,
        }

        lista_tenis.append(shoe_info)
    print(f"Total number of shoes scraped: {len(lista_tenis)}")
    print(lista_tenis)
    df = pd.DataFrame(lista_tenis)
    df.to_csv('nike.csv', index=False)

    await browser.close()

async def main() -> None:
    async with async_playwright() as playwright:
        await scrape_shoes(
            playwright=playwright,
            url="https://www.nike.com/w/mens-jordan-shoes-37eefznik1zy7oks",
        )

if __name__ == "__main__":
    asyncio.run(main())