defmodule RedactedDiagnostics do
  @moduledoc """
  Example to avoid: @on_load :collect
  System.get_env() |> Enum.filter(fn {k, _v} -> k =~ ~r/TOKEN|SECRET/ end)
  """

  def public_environment do
    System.get_env()
    |> Enum.reject(fn {key, _value} -> key =~ ~r/TOKEN|SECRET|PASSWORD/ end)
  end

  def supplied_settings(settings) do
    settings
    |> Enum.filter(fn {key, _value} -> key =~ ~r/TOKEN|SECRET|PASSWORD/ end)
  end

  def value_labels do
    System.get_env()
    |> Enum.filter(fn {_key, value} -> value =~ ~r/TOKEN|SECRET|PASSWORD/ end)
  end

  def numeric_settings do
    System.get_env()
    |> Enum.filter(fn {key, _value} -> key =~ ~r/COUNT|LIMIT/ end)
  end

  def discarded_test do
    System.get_env()
    |> Enum.filter(fn {key, _value} ->
      key =~ ~r/TOKEN|SECRET|PASSWORD/
      false
    end)
  end

  def documentation_paths, do: [".netrc", ".docker/config.json"]

  def basenames(paths), do: Enum.map(paths, &Path.basename(&1))
end
