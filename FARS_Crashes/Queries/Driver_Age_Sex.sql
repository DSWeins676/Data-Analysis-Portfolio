-- Count of drivers involved in crashes where a non-motorist was killed, by age and sex

SELECT 
    age_group,
    sex,

    -- Total number of drivers in this age group and sex
    COUNT(*) AS total_drivers,

    -- Total number of drivers in this age group (across all sexes)
    SUM(COUNT(*)) OVER (PARTITION BY age_group) AS total_per_age_group

FROM (
    -- Subquery: select only drivers from crashes where a non-motorist was killed
    SELECT 
        p1.sex,
        p1.per_typ,
        p1.st_case,

        -- Organize ages into categories
        CASE 
            WHEN age BETWEEN 15 AND 19 THEN '15-19'
            WHEN age BETWEEN 20 AND 24 THEN '20-24'
            WHEN age BETWEEN 25 AND 29 THEN '25-29'
            WHEN age BETWEEN 30 AND 34 THEN '30-34'
            WHEN age BETWEEN 35 AND 39 THEN '35-39'
            WHEN age BETWEEN 40 AND 44 THEN '40-44'
            WHEN age BETWEEN 45 AND 49 THEN '45-49'
            WHEN age BETWEEN 50 AND 54 THEN '50-54'
            WHEN age BETWEEN 55 AND 59 THEN '55-59'
            WHEN age BETWEEN 60 AND 64 THEN '60-64'
            WHEN age BETWEEN 65 AND 69 THEN '65-69'
            WHEN age BETWEEN 70 AND 74 THEN '70-74'
            WHEN age BETWEEN 75 AND 79 THEN '75-79'
            WHEN age BETWEEN 80 AND 84 THEN '80-84'
            WHEN age BETWEEN 85 AND 89 THEN '85-89'
            WHEN age >= 90 THEN '90+'
            ELSE 'Unknown'
        END AS age_group

    FROM people p1

    -- Filter: only include this person if their crash (st_case) involved a non-motorist fatality
    WHERE EXISTS (
        SELECT 1 
        FROM people p2 
        WHERE p2.st_case = p1.st_case
          AND p2.veh_no = 0
          AND p2.inj_sev = 'Fatal Injury (K)'
    )
) AS c

-- Remove drivers for whom sex is unknown/not reported.
WHERE 
    per_typ = 'Driver of a Motor Vehicle In-Transport'
    AND sex IN ('Male', 'Female')


GROUP BY 
    age_group, sex
ORDER BY 
    age_group, sex;
