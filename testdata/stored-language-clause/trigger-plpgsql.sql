CREATE OR REPLACE FUNCTION audit_insert() RETURNS trigger AS $$
BEGIN
  NEW.created_at := now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
