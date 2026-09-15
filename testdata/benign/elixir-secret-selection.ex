defmodule SecretSettings do
  # Selection alone is sensitive configuration handling, not exfiltration.
  def selected do
    System.get_env()
    |> Enum.filter(fn {variable, _value} ->
      variable =~ ~r/TOKEN|SECRET|PASSWORD/
    end)
  end
end
