-- Count of fatal non-motorist crashes by month and time of day
SELECT
 
    DATE_FORMAT(c.crash_date, '%Y-%m') AS crash_month,

    -- Categorize crash as Daytime (between 7:00 and 18:59) or Nighttime (between 19:00 and 6:59 based on crash hour
    CASE 
        WHEN HOUR(c.crash_time) BETWEEN 7 AND 18 THEN 'Daytime'
        ELSE 'Nighttime'
    END AS time_of_day,

    -- Total number of non-motorist fatalities
    COUNT(*) AS total_nonmotorist_fatal

FROM crashes c
INNER JOIN people p ON c.st_case = p.st_case

-- Filter to include only fatal injuries of non-motorists
WHERE 
    p.veh_no = 0 -- Non-motorist indicator
    
    AND p.inj_sev = 'Fatal Injury (K)' -- Fatality Indicator

GROUP BY 
    crash_month, time_of_day
ORDER BY 
    crash_month;
