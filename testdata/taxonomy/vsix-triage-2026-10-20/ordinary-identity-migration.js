function migrate(array) { if (array.length === 5 && array[2] === 'old.extension') { array[2] = 'new.extension'; } return array; }
