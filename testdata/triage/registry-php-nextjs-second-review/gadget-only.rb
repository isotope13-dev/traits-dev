class ChunkBuilder
  def build_chunk(code, ref, property)
    {
      'then' => "$#{ref}:then",
      'status' => 'resolved_model',
      'value' => { 'then' => '$B' }.to_json,
      '_response' => {
        '_prefix' => code,
        '_formData' => { 'get' => "$#{ref}:#{property}" }
      }
    }.to_json
  end
  def property_path(method)
    "#{method}:constructor"
  end
end
