// Real evaluator arguments survive even when the result is invoked.
eval(payload)(argument);
eval(decode(payload))(argument);
