-- Calculate non-motorist fatalities by state and road type

SELECT 
    s.state_name AS State,

    -- Count of urban non-motorist fatalities
    COUNT(CASE 
        WHEN c.rural_urban = 'Urban' THEN 1 
    END) AS Urban_Fatalities,

    -- Percentage of urban non-motorist fatalities
    ROUND(
        100.0 * COUNT(CASE 
            WHEN c.rural_urban = 'Urban' THEN 1 
        END) / COUNT(*), 2
    ) AS Percent_Urban,

    -- Count of rural non-motorist fatalities
    COUNT(CASE 
        WHEN c.rural_urban = 'Rural' THEN 1 
    END) AS Rural_Fatalities,

    -- Percentage of rural non-motorist fatalities
    ROUND(
        100.0 * COUNT(CASE 
            WHEN c.rural_urban = 'Rural' THEN 1 
        END) / COUNT(*), 2
    ) AS Percent_Rural,

    -- Count of non-motorist fatalities in unknown road types
    COUNT(CASE 
        WHEN c.rural_urban NOT IN ('Urban', 'Rural') THEN 1 
    END) AS Unknown_Fatalities,

    -- Percentage of non-motorist fatalities in unknown road types
    ROUND(
        100.0 * COUNT(CASE 
            WHEN c.rural_urban NOT IN ('Urban', 'Rural') THEN 1 
        END) / COUNT(*), 2
    ) AS Percent_Unknown,

    -- Total non-motorist fatalities
    COUNT(*) AS Total_Pedestrian_Fatalities

FROM 
    people p
    INNER JOIN crashes c ON p.st_case = c.st_case
    INNER JOIN states s ON c.state_code = s.state_code

-- Filter to include only non-motorist fatalities
WHERE 
    p.veh_no = 0  -- Non-motorist indicator
    AND p.inj_sev = 'Fatal Injury (K)'  -- Fatality Indicator

GROUP BY 
    s.state_name
ORDER BY 
    s.state_name ASC;
