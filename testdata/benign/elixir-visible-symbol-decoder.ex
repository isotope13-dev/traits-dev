defmodule VisibleSymbolDecoder do
  @alphabet ["a", "b", "c", "d"]

  def byte(symbol) do
    value = Enum.find_index(@alphabet, &(&1 == symbol)) * 64
    :erlang.list_to_binary([value])
  end
end
