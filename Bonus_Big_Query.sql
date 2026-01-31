/*On va dans un premier temps récupérer les tables avec le label 'validated weekly' avant d'analyser le timestamp */
/* On crée une variable qui va stocker du texte*/
DECLARE nom_table STRING;

/* Je trouve la dernière table validée*/
SET nom_table = (
  WITH validated_tables AS (
    SELECT 
      table_name,
      /* Le nom de la table a une structure "ecom_flat_table_20250504050015" */
      /* SUBSTR(table_name, -14) =dcp je prends les 14 derniers caractères du nom */
      /* CAST(...AS INT64) = on transforme ce texte en nombre pour pouvoir comparer les timestamps entre table */
      CAST(SUBSTR(table_name, -14) AS INT64) AS table_timestamp

    FROM `head-of-data-1.assignment_data.INFORMATION_SCHEMA.TABLE_OPTIONS`
        /* Comme il y a plusieurs tables, on garde seulement les tables ecommerce */

    WHERE table_name LIKE 'ecom_flat_table_%'
     /* On regarde ensuite la colonne des labels pour garder ceux des tables validées chaque semaine */
      AND option_name = 'labels'
      AND LOWER(option_value) LIKE '%validated%weekly%'
  )
  /* Maintenant dans la liste validated_tables, on trouve CELLE avec le timestamp max car si on veut le plus récent, il faut prendre le plus gros nombre */
  SELECT table_name
  FROM validated_tables
  ORDER BY table_timestamp DESC
  LIMIT 1
);

/* Maintenant je copie cette table dans MON dataset group_6*/
EXECUTE IMMEDIATE FORMAT("""
  CREATE OR REPLACE TABLE `head-of-data-1.group_6.last_validated_ecom` AS 
  SELECT * FROM `head-of-data-1.assignment_data.%s`
""", nom_table);