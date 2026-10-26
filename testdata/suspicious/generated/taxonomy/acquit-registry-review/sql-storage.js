const query = "INSERT INTO wallets (private_key) VALUES (?)"; db.execute(query, [privateKey]);
