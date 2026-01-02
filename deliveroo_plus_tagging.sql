/* Pour changer le seuil : remplacer tous les 3 par 20 (3 occurrences) */

CREATE OR REPLACE TABLE `group_6.enriched_synthetic_deliveroo_plus_dataset` AS


WITH 
/* On numérote les commandes pour chaque client */
numbered_orders AS (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY id_customer_synth ORDER BY order_datetime_synth) AS row_num,
/* Je numérote aussi les commandes gratuites séparément */
    ROW_NUMBER() OVER (PARTITION BY id_customer_synth, is_free_delivery ORDER BY order_datetime_synth) AS free_row_num
  FROM `assignment_data.synthetic_deliveroo_plus_dataset`

),


/* Pour que les commandes consécutives aient le même sequence_id, on fait la différence entre row_num et free_row_num */
sequences AS (
  SELECT *,
    CASE 
      WHEN is_free_delivery = 1 THEN row_num - free_row_num
/* Pour les commandes payantes chaque ligne a son propre ID */
      ELSE row_num
    END AS sequence_id
  FROM numbered_orders
),

/* Ici on calcule les stats pour chaque séquence */
sequence_stats AS (
  SELECT *,
  /* On compte la longueur de chaque séquence */
    COUNT(*) OVER (PARTITION BY id_customer_synth, sequence_id, is_free_delivery) AS sequence_length,
  /* Date de la première commande de la séquence */
    MIN(order_datetime_synth) OVER (PARTITION BY id_customer_synth, sequence_id, is_free_delivery) AS sequence_start,
    /* Le MAX donne la dernière commande de la séquence */
    MAX(order_datetime_synth) OVER (PARTITION BY id_customer_synth, sequence_id, is_free_delivery) AS sequence_end
  FROM sequences
)


/* Résultat final avec les 3 nouvelles colonnes */
SELECT
  id_customer_synth,
  order_datetime_synth,
  is_free_delivery,

  /* Si gratuit ET au moins 3 dans la séquence = abonné */
  CASE 
    WHEN is_free_delivery = 1 AND sequence_length >= 3 THEN 1
    ELSE 0
  END AS is_order_made_during_subscription,
/* Date de début de l'abonnement */
  CASE 
    WHEN is_free_delivery = 1 AND sequence_length >= 3 THEN sequence_start
    ELSE NULL
  END AS current_subscription_start_datetime,
  /* NULL si pas d'abonnement */
  CASE 
    WHEN is_free_delivery = 1 AND sequence_length >= 3 THEN sequence_end
    ELSE NULL
  END AS current_subscription_end_datetime
FROM sequence_stats
ORDER BY id_customer_synth, order_datetime_synth;