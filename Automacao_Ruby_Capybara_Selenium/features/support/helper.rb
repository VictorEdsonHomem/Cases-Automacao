require "fileutils"

module Helper
  def take_screenshot(file_name, result)
    timer_path = Time.now.strftime("%F").to_s
    file_path = "results/screenshots/test_#{result}/run_#{timer_path}"
    screenshot = "#{file_path}/#{file_name}.png"
    page.save_screenshot(screenshot)
    attach(screenshot, 'image/png')
  end
end

def wait_for_ajax
  Timeout.timeout(Capybara.default_max_wait_time) do
    loop do
      active = page.evaluate_script("jQuery.active")
      break if active == 0
    end
  end
end

def maximixe_browser
  Capybara.page.driver.browser.manage.window.maximize
end

def normalizar_path(path)
  File.join(Dir.pwd, path).gsub(File::SEPARATOR, File::ALT_SEPARATOR || File::SEPARATOR)
end

def gravar_dados(path, dados)
  @path_file = normalizar_path(path).downcase

  File.open(@path_file, "w") do |file|
    file.puts(dados)
  end
end

def recuperar_dados(file)
  File.readlines(file)
end

def atualizar_conteudo(path, dados)
  @path_file = normalizar_path(path)

  File.open(@path_file, "a") do |file|
    file.puts(dados)
  end
end

def anexar(campo_anexar, path)
  @path_file = normalizar_path(path)
  attach_file(campo_anexar, @path_file, make_visible: true)
end

