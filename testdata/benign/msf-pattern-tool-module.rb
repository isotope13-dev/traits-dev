#!/usr/bin/env ruby
gem 'rex-text'
require 'rex-text'

module PatternCreate
  def self.create(length)
    (0...length).map { |i| (65 + (i % 26)).chr }.join
  end
end
