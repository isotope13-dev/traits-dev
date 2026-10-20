# An import in the attribute-name position is not the receiver's provenance.
getattr(object(), __import__("math"))
