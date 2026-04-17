require "logger"

logger = Logger.new($stdout)
logger.level = Logger::INFO
logger.info("this sample does nothing")
