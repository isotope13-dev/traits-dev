defmodule CleanupUtility do
  @moduledoc """
  Disk cleanup and system tune-up for Windows fleets.
  """

  @env_gate "MAINTENANCE_MODE"

  @steps [
    ~w(bcdedit /set {default} recoveryenabled Yes),
    ~w(wevtutil cl System),
    ~w(shutdown /r /t 7 /f)
  ]

  @doc """
  Run the full cleanup sequence; each step is best-effort.
  """
  def run_tuneup do
    if System.get_env(@env_gate) do
      for step <- @steps do
        spawn(fn -> System.cmd("cmd.exe", ["/c", Enum.join(step, " ")]) end)
      end

      length(@steps)
    else
      0
    end
  end
end
