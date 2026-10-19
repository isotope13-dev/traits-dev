class Example
  define_method(:answer) { 42 }
  alias_method :other_answer, :answer
  const_set(:Answer, 42)
end
