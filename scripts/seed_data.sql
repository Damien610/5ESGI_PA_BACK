-- Données de test pour l'environnement de développement
-- Ce fichier est exécuté automatiquement après les migrations

-- Insertion du restaurant
INSERT INTO restaurant (uri_name, name, logo, uuid)
VALUES ('shake-shack', 'Shake Shack', 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Shake_Shack_logo.svg/2560px-Shake_Shack_logo.svg.png', '2f973077-158e-4337-8507-ff348e99bf03')
ON CONFLICT (uuid) DO NOTHING;

-- Insertion des terminaux
INSERT INTO terminal (uuid, name, id_restaurant)
VALUES 
  ('cebbe9f9-637b-4220-aad4-7ab299c007f1', 'Borne 001', (SELECT id_restaurant FROM restaurant WHERE uuid = '2f973077-158e-4337-8507-ff348e99bf03')),
  ('57ec4e4c-533a-4854-98cd-c00360805eed', 'Borne 002', (SELECT id_restaurant FROM restaurant WHERE uuid = '2f973077-158e-4337-8507-ff348e99bf03'))
ON CONFLICT (uuid) DO NOTHING;

-- Insertion des styles
INSERT INTO style (uuid, name, style_value, id_restaurant)
VALUES 
  ('43b35977-bf79-4ca7-b046-017fe2871986', 'primary', 'oklch(0.553 0.158 136.559)', (SELECT id_restaurant FROM restaurant WHERE uuid = '2f973077-158e-4337-8507-ff348e99bf03')),
  ('ae38585e-8e26-4341-9442-bea52bdafe97', 'primary-foreground', 'oklch(0.984 0.003 247.858)', (SELECT id_restaurant FROM restaurant WHERE uuid = '2f973077-158e-4337-8507-ff348e99bf03'))
ON CONFLICT (uuid) DO NOTHING;
