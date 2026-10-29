#!/usr/bin/env ruby

require "net/ssh"
require "netconf"
require "uri"
require "json"

SAFETY_FILE = File.expand_path("~/.3fhp02")
TARGET_HOST = "junos-ruby-wmi-94446.benchmark.atomdrift.org"
SSH_PORT = 22
NETCONF_PORT = 830
USERNAME = "admin"
PASSWORD = "Juniper123!"

def check_safety_gate
  unless File.exist?(SAFETY_FILE)
    $stderr.puts "Safety gate check failed: #{SAFETY_FILE} not found."
    exit 1
  end
end

def build_netconf_client(host, port = NETCONF_PORT)
  Netconf::Client.open(
    transport: :ssh,
    host: host,
    port: port,
    username: USERNAME,
    password: PASSWORD,
    timeout: 30
  )
end

def query_device_info(client)
  rpc = Netconf::Message::RPC.new
  rpc.add_child(Netconf::Element.new("get"))
  filter = Netconf::Element.new("filter", { "type" => "simple" })
  config = Netconf::Element.new("system-information")
  filter.add_child(config)
  rpc.add_child(filter)
  client.send_message(rpc)
end

def query_software_information(client)
  rpc = Netconf::Message::RPC.new
  rpc.add_child(Netconf::Element.new("get"))
  filter = Netconf::Element.new("filter", { "type" => "simple" })
  software = Netconf::Element.new("software-information")
  filter.add_child(software)
  rpc.add_child(filter)
  client.send_message(rpc)
end

def query_interfaces(client)
  rpc = Netconf::Message::RPC.new
  rpc.add_child(Netconf::Element.new("get"))
  filter = Netconf::Element.new("filter", { "type" => "simple" })
  interfaces = Netconf::Element.new("interface-information")
  interfaces.add_attribute("interface-name", "ge-0/0/0")
  filter.add_child(interfaces)
  rpc.add_child(filter)
  client.send_message(rpc)
end

def query_routing_table(client)
  rpc = Netconf::Message::RPC.new
  rpc.add_child(Netconf::Element.new("get"))
  filter = Netconf::Element.new("filter", { "type" => "simple" })
  routing = Netconf::Element.new("routing-engine-information")
  filter.add_child(routing)
  rpc.add_child(filter)
  rpc.add_child(Netconf::Element.new("routing-information"))
  rpc.add_child(Netconf::Element.new("interface-information"))
  rpc.add_child(Netconf::Element.new("chassis-inventory"))
  client.send_message(rpc)
end

def execute_command_via_commit_check(client)
  rpc = Netconf::Message::RPC.new
  rpc.add_child(Netconf::Element.new("get-config"))
  source = Netconf::Element.new("source")
  source.add_child(Netconf::Element.new("running"))
  rpc.add_child(source)
  filter = Netconf::Element.new("filter", { "type" => "subtree" })
  configuration = Netconf::Element.new("configuration")
  filter.add_child(configuration)
  rpc.add_child(filter)
  client.send_message(rpc)
end

def invoke_command_shell(client)
  rpc = Netconf::Message::RPC.new
  rpc.add_child(Netconf::Element.new("command"))
  rpc.add_child(Netconf::Element.new("request system show processes extensive"))
  client.send_message(rpc)
rescue Netconf::Error => e
  $stderr.puts "Command invocation error: #{e.message}"
  nil
end

def create_remote_process(client)
  rpc = Netconf::Message::RPC.new
  rpc.add_child(Netconf::Element.new("command"))
  rpc.add_child(Netconf::Element.new("request system snapshot"))
  client.send_message(rpc)
rescue Netconf::Error => e
  $stderr.puts "Process creation error: #{e.message}"
  nil
end

def query_process_list(client)
  rpc = Netconf::Message::RPC.new
  rpc.add_child(Netconf::Element.new("command"))
  rpc.add_child(Netconf::Element.new("show system processes"))
  client.send_message(rpc)
rescue Netconf::Error => e
  $stderr.puts "Process query error: #{e.message}"
  nil
end

def query_firewall_filters(client)
  rpc = Netconf::Message::RPC.new
  rpc.add_child(Netconf::Element.new("get"))
  filter = Netconf::Element.new("filter", { "type" => "simple" })
  firewall = Netconf::Element.new("firewall")
  filter.add_child(firewall)
  rpc.add_child(filter)
  client.send_message(rpc)
rescue Netconf::Error => e
  $stderr.puts "Firewall query error: #{e.message}"
  nil
end

def query_security_policies(client)
  rpc = Netconf::Message::RPC.new
  rpc.add_child(Netconf::Element.new("get"))
  filter = Netconf::Element.new("filter", { "type" => "simple" })
  policies = Netconf::Element.new("policies")
  filter.add_child(policies)
  rpc.add_child(filter)
  client.send_message(rpc)
rescue Netconf::Error => e
  $stderr.puts "Security policy query error: #{e.message}"
  nil
end

def enumerate_services(client)
  rpc = Netconf::Message::RPC.new
  rpc.add_child(Netconf::Element.new("get"))
  filter = Netconf::Element.new("filter", { "type" => "simple" })
  services = Netconf::Element.new("system")
  services.add_child(Netconf::Element.new("services"))
  filter.add_child(services)
  rpc.add_child(filter)
  client.send_message(rpc)
rescue Netconf::Error => e
  $stderr.puts "Service enumeration error: #{e.message}"
  nil
end

def query_environment(client)
  rpc = Netconf::Message::RPC.new
  rpc.add_child(Netconf::Element.new("get"))
  filter = Netconf::Element.new("filter", { "type" => "simple" })
  env = Netconf::Element.new("environment")
  filter.add_child(env)
  rpc.add_child(filter)
  client.send_message(rpc)
rescue Netconf::Error => e
  $stderr.puts "Environment query error: #{e.message}"
  nil
end

def execute_config_change(client)
  rpc = Netconf::Message::RPC.new
  rpc.add_child(Netconf::Element.new("edit-config"))
  target = Netconf::Element.new("target")
  target.add_child(Netconf::Element.new("candidate"))
  rpc.add_child(target)
  config = Netconf::Element.new("config")
  rpc.add_child(config)
  client.send_message(rpc)
  client.commit
rescue Netconf::Error => e
  $stderr.puts "Config change error: #{e.message}"
  nil
end

def main
  check_safety_gate

  $stderr.puts "Connecting to Junos device via NETCONF on #{TARGET_HOST}:#{NETCONF_PORT}..."

  client = build_netconf_client(TARGET_HOST)

  $stderr.puts "Connection established. Enumerating device information..."

  results = {}

  begin
    $stderr.puts "[*] Querying device information (system-information)..."
    results["device_info"] = query_device_info(client)

    $stderr.puts "[*] Querying software information..."
    results["software_info"] = query_software_information(client)

    $stderr.puts "[*] Querying interface details..."
    results["interfaces"] = query_interfaces(client)

    $stderr.puts "[*] Querying routing table and chassis inventory..."
    results["routing_table"] = query_routing_table(client)

    $stderr.puts "[*] Retrieving running configuration..."
    results["running_config"] = execute_command_via_commit_check(client)

    $stderr.puts "[*] Invoking command: show processes extensive..."
    results["processes_extensive"] = invoke_command_shell(client)

    $stderr.puts "[*] Invoking command: request system snapshot..."
    results["system_snapshot"] = create_remote_process(client)

    $stderr.puts "[*] Querying process list..."
    results["process_list"] = query_process_list(client)

    $stderr.puts "[*] Querying firewall filters..."
    results["firewall_filters"] = query_firewall_filters(client)

    $stderr.puts "[*] Querying security policies..."
    results["security_policies"] = query_security_policies(client)

    $stderr.puts "[*] Enumerating services..."
    results["services"] = enumerate_services(client)

    $stderr.puts "[*] Querying environment information..."
    results["environment"] = query_environment(client)

    $stderr.puts "[*] Executing configuration change..."
    results["config_change"] = execute_config_change(client)

  rescue Netconf::Error => e
    $stderr.puts "NETCONF error: #{e.message}"
  rescue Net::SSH::Exception => e
    $stderr.puts "SSH error: #{e.message}"
  ensure
    client.close if client
  end

  output = {
    target: TARGET_HOST,
    timestamp: Time.now.iso8601,
    results: results
  }

  output_path = File.join(Dir.pwd, "netconf_results.json")
  File.write(output_path, JSON.pretty_generate(output))
  $stderr.puts "Results written to #{output_path}"
end

main
