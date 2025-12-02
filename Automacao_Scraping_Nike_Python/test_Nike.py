import asyncio
import pandas as pd
from playwright.async_api import Playwright, async_playwright

async def scrape_shoes(playwright: Playwright, url: str) -> None:
    """
    Função principal que realiza o web scraping dos tênis do site da Nike.
    
    Args:
        playwright: Instância do Playwright para controle do navegador
        url: URL da página de tênis que será raspada
    """
    
    # Inicializa o navegador Chromium em modo visível (headless=False)
    browser = await playwright.chromium.launch(headless=False)
    
    # Cria uma nova página com viewport definido para resolução Full HD
    page = await browser.new_page(viewport={"width": 1920, "height": 1080})

    # Navega até a URL fornecida
    await page.goto(url)

    # Lista para armazenar os dados coletados de cada tênis
    lista_tenis = []

    # Localiza todos os elementos que representam cards de produtos
    container_tenis = await page.query_selector_all(".product-card")

    # Itera sobre cada card de tênis encontrado
    for tenis in container_tenis:
        # Extrai o nome do tênis usando o seletor CSS apropriado
        nome_tenis = await tenis.query_selector(".product-card__title")
        nome_tenis = await nome_tenis.text_content() if nome_tenis else "N/A"

        # Extrai o preço do tênis
        preco_tenis = await tenis.query_selector(".product-price")
        preco_tenis = await preco_tenis.text_content() if preco_tenis else "N/A"

        # Extrai a quantidade de cores disponíveis
        cor_tenis = await tenis.query_selector(".product-card__product-count")
        cor_tenis = await cor_tenis.text_content() if cor_tenis else "N/A"

        # Extrai o status do produto (disponibilidade, promoção, etc)
        status_tenis = await tenis.query_selector(".product-card__messaging")
        status_tenis = await status_tenis.text_content() if status_tenis else "N/A"

        # Extrai o link para a página do produto
        link_tenis = await tenis.query_selector(".product-card__link-overlay")
        link_tenis = await link_tenis.get_attribute("href") if link_tenis else "N/A"

        # Cria um dicionário com as informações coletadas do tênis
        shoe_info = {
            "nome": nome_tenis,
            "preco": preco_tenis,
            "cor": cor_tenis,
            "status": status_tenis,
            "link": link_tenis,
        }

        # Adiciona as informações à lista de tênis
        lista_tenis.append(shoe_info)
    
    # Exibe informações sobre a raspagem no console
    print(f"Total number of shoes scraped: {len(lista_tenis)}")
    print(lista_tenis)
    
    # Converte a lista de dicionários para um DataFrame do pandas
    df = pd.DataFrame(lista_tenis)
    
    # Salva os dados em um arquivo CSV
    df.to_csv('resultado_nike.csv', index=False)

    # Fecha o navegador
    await browser.close()

async def main() -> None:
    """
    Função principal que gerencia o contexto do Playwright e chama a função de scraping.
    Utiliza async with para gerenciar automaticamente o ciclo de vida do Playwright.
    """
    async with async_playwright() as playwright:
        # Chama a função de scraping com a URL específica dos tênis Jordan masculinos
        await scrape_shoes(
            playwright=playwright,
            url="https://www.nike.com/w/mens-jordan-shoes-37eefznik1zy7oks",
        )

if __name__ == "__main__":
    """
    Ponto de entrada do programa. Executa a função main de forma assíncrona.
    O asyncio.run() é responsável por iniciar e gerenciar o loop de eventos.
    """
    asyncio.run(main())