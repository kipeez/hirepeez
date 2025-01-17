CREATE ROLE app;
ALTER DEFAULT PRIVILEGES FOR ROLE app GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app;

GRANT CONNECT ON DATABASE aidvizdb TO app;
GRANT USAGE ON SCHEMA public TO app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app;


CREATE USER api_user WITH LOGIN PASSWORD '...';
GRANT app TO api_user;