CREATE TABLE IF NOT EXISTS organisations (
    id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT,
    slug TEXT,
    created_at DATE DEFAULT CURRENT_DATE,
    owner_id UUID REFERENCES users(id)
);
CREATE TABLE user_organisations (
    user_id UUID REFERENCES users(id),
    organisation_id UUID REFERENCES organisations(id),
    PRIMARY KEY (user_id, organisation_id)
);

CREATE UNIQUE INDEX user_organisations_idx on user_organisations (user_id, organisation_id);



CREATE TABLE organisation_invitations (
    id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
    organisation_id UUID REFERENCES organisations(id),
    sender_id UUID REFERENCES users(id),
    guest_email TEXT,
    send_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(0)::TIMESTAMP WITHOUT TIME ZONE,
    accepted_at TIMESTAMP
);

CREATE UNIQUE INDEX organisation_invitations_idx on organisation_invitations (organisation_id, sender_id, guest_email);
