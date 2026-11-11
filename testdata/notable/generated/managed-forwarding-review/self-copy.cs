class Copier { void Go(Stream a) { Task.WhenAll(a.CopyToAsync(a),a.CopyToAsync(a)); } }
