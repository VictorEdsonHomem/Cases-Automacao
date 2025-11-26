require "capybara"
require "capybara/cucumber"
require "capybara/rspec"
require "rspec"
require "selenium-webdriver"
require "webdrivers"
require "pry"
require "faker"
require "cpf_faker"
require "rubocop-faker"
require "timeout"

# require 'allure-cucumber'

require_relative "helper.rb"

World(Capybara::DSL) #DSLs globais para o Capybara
$logger = Logger.new(STDOUT)

CUCUMBER_PUBLISH_ENABLED = true

HEADLESS = ENV["HEADLESS"]

CONFIG = YAML.load_file(File.dirname(__FILE__) + "/data/homologacao.yml")


Capybara.register_driver :firefox do |app|

  client = Selenium::WebDriver::Remote::Http::Default.new
  client.read_timeout = 300

  Capybara::Selenium::Driver.new(
    app,      
    browser: :firefox,
    :http_client => client,
    clear_local_storage: true,
    clear_session_storage: true,
    options: browser_options = ::Selenium::WebDriver::Firefox::Options.new(
      binary: 'C:\Program Files\Mozilla Firefox\firefox.exe'
      #args: ['--headless']
    )
  )
  
end

Capybara.configure do |config| #config da instância para o Capybara
  $logger.info("Instaciando o driver e acessando a host-url")

  config.default_driver = :firefox
  config.default_max_wait_time = 30
  config.app_host = CONFIG["url_padrao"]
  Capybara.page.driver.browser.manage.window.maximize
end

