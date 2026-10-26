function walk(x){ x.touch(); if(!x.parent) return; x.touch(); walk(x.parent); }
