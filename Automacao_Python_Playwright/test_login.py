import base64
import os
from playwright.sync_api import Playwright, sync_playwright, expect
import datetime

def image_to_base64(image_path):
    """Converte imagem para base64 para embedar no HTML"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Erro ao converter imagem: {e}")
        return None

def generate_html_report(test_results):
    """Gera um relatório HTML com os resultados dos testes"""
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Relatório de Testes - Login</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
            .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            .header {{ text-align: center; padding: 20px; background: #2c3e50; color: white; border-radius: 8px; margin-bottom: 20px; }}
            .summary {{ display: flex; justify-content: space-around; margin: 20px 0; }}
            .summary-item {{ text-align: center; padding: 15px; border-radius: 8px; }}
            .passed {{ background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }}
            .failed {{ background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }}
            .total {{ background: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; }}
            .test-case {{ margin: 15px 0; padding: 15px; border-radius: 8px; border-left: 5px solid; }}
            .test-passed {{ border-left-color: #28a745; background: #f8fff9; }}
            .test-failed {{ border-left-color: #dc3545; background: #fff8f8; }}
            .screenshot {{ max-width: 400px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; cursor: pointer; }}
            .screenshot:hover {{ transform: scale(1.02); transition: transform 0.2s; }}
            .timestamp {{ text-align: center; color: #666; font-size: 0.9em; margin-top: 20px; }}
            .screenshot-section {{ margin: 10px 0; }}
            .screenshot-title {{ font-weight: bold; margin-bottom: 5px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Relatório de Testes - Sistema de Login</h1>
                <p>Testes automatizados com Python e Playwright</p>
            </div>
            
            <div class="summary">
                <div class="summary-item total">
                    <h3>Total</h3>
                    <p>{len(test_results)}</p>
                </div>
                <div class="summary-item passed">
                    <h3>Passaram</h3>
                    <p>{sum(1 for test in test_results if test['status'] == 'PASS')}</p>
                </div>
                <div class="summary-item failed">
                    <h3>Falharam</h3>
                    <p>{sum(1 for test in test_results if test['status'] == 'FAIL')}</p>
                </div>
            </div>
    """
    
    for i, test in enumerate(test_results, 1):
        status_class = "test-passed" if test['status'] == 'PASS' else "test-failed"
        status_text = "✅ PASSOU" if test['status'] == 'PASS' else "❌ FALHOU"
        
        html_content += f"""
            <div class="test-case {status_class}">
                <h3>Teste {i}: {test['name']} - {status_text}</h3>
                <p><strong>Cenário:</strong> {test['scenario']}</p>
                <p><strong>Descrição:</strong> {test['description']}</p>
                <p><strong>Resultado Esperado:</strong> {test['expected']}</p>
                <p><strong>Resultado Obtido:</strong> {test['actual']}</p>
                <p><strong>Tempo de Execução:</strong> {test['duration']:.2f} segundos</p>
        """
        
        # Adicionar screenshot se existir
        if test.get('screenshot') and os.path.exists(test['screenshot']):
            base64_image = image_to_base64(test['screenshot'])
            if base64_image:
                html_content += f"""
                <div class="screenshot-section">
                    <div class="screenshot-title">Evidência:</div>
                    <img src="data:image/png;base64,{base64_image}" 
                         class="screenshot" 
                         alt="Screenshot do teste {i}"
                         title="Clique para ampliar">
                </div>
                """
        
        html_content += "</div>"
    
    html_content += f"""
            <div class="timestamp">
                <p>Relatório gerado em: {timestamp}</p>
            </div>
        </div>
        
        <script>
            // Script para ampliar screenshots ao clicar
            document.addEventListener('DOMContentLoaded', function() {{
                const screenshots = document.querySelectorAll('.screenshot');
                screenshots.forEach(img => {{
                    img.addEventListener('click', function() {{
                        if (this.style.maxWidth === '90vw') {{
                            this.style.maxWidth = '400px';
                            this.style.position = 'static';
                            this.style.zIndex = 'auto';
                        }} else {{
                            this.style.maxWidth = '90vw';
                            this.style.position = 'fixed';
                            this.style.top = '50%';
                            this.style.left = '50%';
                            this.style.transform = 'translate(-50%, -50%)';
                            this.style.zIndex = '1000';
                            this.style.background = 'white';
                            this.style.padding = '10px';
                            this.style.borderRadius = '8px';
                            this.style.boxShadow = '0 0 20px rgba(0,0,0,0.5)';
                        }}
                    }});
                }});
            }});
        </script>
    </body>
    </html>
    """
    
    # Criar diretório para relatórios se não existir
    os.makedirs("reports", exist_ok=True)
    
    # Salvar relatório
    filename = f"reports/test_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"Relatório HTML gerado: {filename}")
    return filename

def run_tests(playwright: Playwright) -> dict:
    """Executa os testes e retorna os resultados"""
    
    test_results = []
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    try:
        # Teste 1: Login com sucesso
        start_time = datetime.datetime.now()
        test_name = "Login com credenciais válidas"
        
        try:
            page.goto("https://practicetestautomation.com/practice-test-login/", wait_until='networkidle')
            expect(page.locator("#site-title")).to_be_visible()
            page.get_by_role("textbox", name="Username").click()
            page.get_by_role("textbox", name="Username").fill("student")
            page.get_by_role("textbox", name="Password").click()
            page.get_by_role("textbox", name="Password").fill("Password123")
            page.get_by_role("button", name="Submit").click()
            
            # Aguardar o login completar
            page.wait_for_url("**/logged-in-successfully/")
            expect(page.get_by_role("heading", name="Logged In Successfully")).to_be_visible()
            expect(page.get_by_role("link", name="Log out")).to_be_visible()
            
            # Tirar screenshot como evidência
            os.makedirs("screenshots", exist_ok=True)
            screenshot_path = f"screenshots/login_success_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            page.screenshot(path=screenshot_path, full_page=True)
            
            page.get_by_role("link", name="Log out").click()
            
            end_time = datetime.datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            test_results.append({
                'name': test_name,
                'status': 'PASS',
                'scenario': 'Login válido',
                'description': 'Login com usuário e senha corretos',
                'expected': 'Usuário deve fazer login com sucesso e ver a página de sucesso',
                'actual': 'Login realizado com sucesso, página de sucesso exibida',
                'duration': duration,
                'screenshot': screenshot_path
            })
            
        except Exception as e:
            end_time = datetime.datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # Tirar screenshot do erro
            screenshot_path = f"screenshots/error_login_success_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            page.screenshot(path=screenshot_path, full_page=True)
            
            test_results.append({
                'name': test_name,
                'status': 'FAIL',
                'scenario': 'Login válido',
                'description': 'Login com usuário e senha corretos',
                'expected': 'Usuário deve fazer login com sucesso e ver a página de sucesso',
                'actual': f'Falha no login: {str(e)}',
                'duration': duration,
                'screenshot': screenshot_path
            })

        # Teste 2: Login com usuário incorreto
        start_time = datetime.datetime.now()
        test_name = "Login com usuário inválido"
        
        try:
            page.get_by_role("textbox", name="Username").click()
            page.get_by_role("textbox", name="Username").fill("testeERRO")
            page.get_by_role("textbox", name="Password").click()
            page.get_by_role("textbox", name="Password").fill("Password123")
            page.get_by_role("button", name="Submit").click()
            
            # Aguardar a mensagem de erro
            page.wait_for_selector("#error", state="visible")
            expect(page.locator("#error")).to_be_visible()
            
            # Verificar mensagem de erro
            error_message = page.locator("#error").text_content()
            expected_error = "Your username is invalid!"
            
            if expected_error in error_message:
                screenshot_path = f"screenshots/login_user_error_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                page.screenshot(path=screenshot_path, full_page=True)
                
                end_time = datetime.datetime.now()
                duration = (end_time - start_time).total_seconds()
                
                test_results.append({
                    'name': test_name,
                    'status': 'PASS',
                    'scenario': 'Login inválido - usuário incorreto',
                    'description': 'Login com usuário incorreto e senha correta',
                    'expected': 'Sistema deve exibir mensagem de erro de usuário inválido',
                    'actual': f'Mensagem de erro exibida: {error_message.strip()}',
                    'duration': duration,
                    'screenshot': screenshot_path
                })
            else:
                raise Exception(f"Mensagem de erro incorreta. Esperado: '{expected_error}', Obtido: '{error_message}'")
                
        except Exception as e:
            end_time = datetime.datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            screenshot_path = f"screenshots/error_user_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            page.screenshot(path=screenshot_path, full_page=True)
            
            test_results.append({
                'name': test_name,
                'status': 'FAIL',
                'scenario': 'Login inválido - usuário incorreto',
                'description': 'Login com usuário incorreto e senha correta',
                'expected': 'Sistema deve exibir mensagem de erro de usuário inválido',
                'actual': f'Falha no teste: {str(e)}',
                'duration': duration,
                'screenshot': screenshot_path
            })

        # Teste 3: Login com senha incorreta
        start_time = datetime.datetime.now()
        test_name = "Login com senha inválida"
        
        try:
            page.get_by_role("textbox", name="Username").click()
            page.get_by_role("textbox", name="Username").fill("student")
            page.get_by_role("textbox", name="Password").click()
            page.get_by_role("textbox", name="Password").fill("testeERRO")
            page.get_by_role("button", name="Submit").click()
            
            # Aguardar a mensagem de erro
            page.wait_for_selector("#error", state="visible")
            expect(page.locator("#error")).to_be_visible()
            
            # Verificar mensagem de erro
            error_message = page.locator("#error").text_content()
            expected_error = "Your password is invalid!"
            
            if expected_error in error_message:
                screenshot_path = f"screenshots/login_password_error_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                page.screenshot(path=screenshot_path, full_page=True)
                
                end_time = datetime.datetime.now()
                duration = (end_time - start_time).total_seconds()
                
                test_results.append({
                    'name': test_name,
                    'status': 'PASS',
                    'scenario': 'Login inválido - senha incorreta',
                    'description': 'Login com usuário correto e senha incorreta',
                    'expected': 'Sistema deve exibir mensagem de erro de senha inválida',
                    'actual': f'Mensagem de erro exibida: {error_message.strip()}',
                    'duration': duration,
                    'screenshot': screenshot_path
                })
            else:
                raise Exception(f"Mensagem de erro incorreta. Esperado: '{expected_error}', Obtido: '{error_message}'")
                
        except Exception as e:
            end_time = datetime.datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            screenshot_path = f"screenshots/error_password_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            page.screenshot(path=screenshot_path, full_page=True)
            
            test_results.append({
                'name': test_name,
                'status': 'FAIL',
                'scenario': 'Login inválido - senha incorreta',
                'description': 'Login com usuário correto e senha incorreta',
                'expected': 'Sistema deve exibir mensagem de erro de senha inválida',
                'actual': f'Falha no teste: {str(e)}',
                'duration': duration,
                'screenshot': screenshot_path
            })

    finally:
        # Fechar browser
        context.close()
        browser.close()
    
    return test_results

def main():
    """Função principal que executa os testes e gera o relatório"""
    
    print("Iniciando execução dos testes...")
    
    with sync_playwright() as playwright:
        test_results = run_tests(playwright)
    
    # Gerar relatório HTML
    report_file = generate_html_report(test_results)
    
    # Resumo no console
    passed = sum(1 for test in test_results if test['status'] == 'PASS')
    failed = sum(1 for test in test_results if test['status'] == 'FAIL')
    
    print(f"\n=== RESUMO DOS TESTES ===")
    print(f"Total: {len(test_results)}")
    print(f"Passaram: {passed}")
    print(f"Falharam: {failed}")
    print(f"Relatório HTML: {report_file}")
    
    # Abrir o relatório automaticamente no navegador
    import webbrowser
    webbrowser.open(f'file://{os.path.abspath(report_file)}')

if __name__ == "__main__":
    main()