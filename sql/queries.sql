-- =============================================
-- AUTO INSURANCE LOSS ANALYSIS
-- SQL Queries
-- =============================================

-- 1. BOOK LEVEL SUMMARY
SELECT
    COUNT(*) as total_policies,
    ROUND(SUM(Exposure), 1) as total_exposure,
    SUM(ClaimNb) as total_claims,
    ROUND(SUM(ClaimAmount), 0) as total_losses,
    ROUND(SUM(ClaimAmount) / SUM(ClaimNb), 2) as avg_severity,
    ROUND(SUM(ClaimNb) / SUM(Exposure), 4) as claim_frequency
FROM policies;

-- 2. LOSS RATIO BY DRIVER AGE GROUP
SELECT
    CASE
        WHEN DrivAge BETWEEN 18 AND 25 THEN '18-25'
        WHEN DrivAge BETWEEN 26 AND 35 THEN '26-35'
        WHEN DrivAge BETWEEN 36 AND 50 THEN '36-50'
        WHEN DrivAge BETWEEN 51 AND 65 THEN '51-65'
        ELSE '65+'
    END as AgeGroup,
    COUNT(*) as policies,
    ROUND(SUM(ClaimNb) / SUM(Exposure), 4) as frequency,
    ROUND(SUM(ClaimAmount) / SUM(ClaimNb), 2) as severity,
    ROUND(SUM(500.0 * (BonusMalus/100.0) * Exposure), 0) as premium,
    ROUND(SUM(ClaimAmount) / SUM(500.0 * (BonusMalus/100.0) * Exposure) * 100, 2) as loss_ratio
FROM policies
GROUP BY AgeGroup
ORDER BY loss_ratio DESC;

-- 3. LOSS RATIO BY AREA
SELECT
    Area,
    COUNT(*) as policies,
    ROUND(SUM(ClaimNb) / SUM(Exposure), 4) as frequency,
    ROUND(SUM(ClaimAmount) / SUM(ClaimNb), 2) as severity,
    ROUND(SUM(ClaimAmount) / SUM(500.0 * (BonusMalus/100.0) * Exposure) * 100, 2) as loss_ratio
FROM policies
GROUP BY Area
ORDER BY loss_ratio DESC;

-- 4. TOP 10 HIGHEST LOSS POLICIES
SELECT
    IDpol,
    DrivAge,
    VehAge,
    Area,
    BonusMalus,
    ClaimNb,
    ROUND(ClaimAmount, 0) as total_losses,
    ROUND(500.0 * (BonusMalus/100.0) * Exposure, 0) as premium,
    ROUND(ClaimAmount / (500.0 * (BonusMalus/100.0) * Exposure) * 100, 1) as loss_ratio
FROM policies
WHERE ClaimAmount > 0
ORDER BY ClaimAmount DESC
LIMIT 10;

-- 5. PARETO - LOSS CONCENTRATION
SELECT
    CASE
        WHEN ClaimAmount = 0 THEN 'No Claim'
        WHEN ClaimAmount < 1000 THEN 'Under 1K'
        WHEN ClaimAmount < 5000 THEN '1K-5K'
        WHEN ClaimAmount < 10000 THEN '5K-10K'
        ELSE 'Over 10K'
    END as loss_bucket,
    COUNT(*) as policies,
    ROUND(SUM(ClaimAmount), 0) as total_losses,
    ROUND(SUM(ClaimAmount) * 100.0 / (SELECT SUM(ClaimAmount) FROM policies), 2) as pct_of_total_losses
FROM policies
GROUP BY loss_bucket
ORDER BY total_losses DESC;