/*
============================================================
PROJECT: Student Study Habits Analyzer
DATABASE: student_performance_analysis
TABLE: public.student_study_habits_clean
PURPOSE: Analyze student study habits, attendance,
         time management, procrastination, and data quality.
============================================================
*/


-- ==========================================================
-- 1. DATABASE VERIFICATION
-- Check that queries are running in the intended database.
-- ==========================================================

SELECT current_database();


-- ==========================================================
-- 2. TOTAL STUDENT COUNT
-- Count the total number of records in the cleaned dataset.
-- ==========================================================

SELECT
    COUNT(*) AS total_students
FROM public.student_study_habits_clean;


-- ==========================================================
-- 3. STUDY HABIT ANALYSIS
-- Count students in each study-hours category.
-- Results are sorted from largest to smallest group.
-- ==========================================================

SELECT
    study_category,
    COUNT(*) AS student_count
FROM public.student_study_habits_clean
GROUP BY study_category
ORDER BY student_count DESC;


-- ==========================================================
-- 4. ATTENDANCE DISTRIBUTION
-- Count students in each attendance category.
-- ==========================================================

SELECT
    attendance_category,
    COUNT(*) AS student_count
FROM public.student_study_habits_clean
GROUP BY attendance_category
ORDER BY student_count DESC;


-- ==========================================================
-- 5. TIME MANAGEMENT ANALYSIS
-- Count students in each time-management category.
-- ==========================================================

SELECT
    time_management_category,
    COUNT(*) AS student_count
FROM public.student_study_habits_clean
GROUP BY time_management_category
ORDER BY student_count DESC;


-- ==========================================================
-- 6. PROCRASTINATION ANALYSIS
-- Count students by their reported procrastination level.
-- NULL values, if present, are grouped separately.
-- ==========================================================

SELECT
    how_often_do_you_procrastinate AS procrastination_level,
    COUNT(*) AS student_count
FROM public.student_study_habits_clean
GROUP BY how_often_do_you_procrastinate
ORDER BY student_count DESC;


-- ==========================================================
-- 7. DATA QUALITY CHECK
-- Count missing physical activity and procrastination values.
-- For the biggest-challenge field, count both NULL and
-- blank/whitespace-only values as missing.
-- ==========================================================

SELECT
    COUNT(*) FILTER (
        WHERE average_physical_activity_per_week IS NULL
    ) AS missing_physical_activity,

    COUNT(*) FILTER (
        WHERE how_often_do_you_procrastinate IS NULL
    ) AS missing_procrastination,

    COUNT(*) FILTER (
        WHERE NULLIF(
            TRIM(
                what_do_you_think_is_the_biggest_challenge_affecting_your_studies
            ),
            ''
        ) IS NULL
    ) AS missing_biggest_challenge

FROM public.student_study_habits_clean;


-- ==========================================================
-- 8. ATTENDANCE VS. RECORDED ACADEMIC SCORE
-- Calculate the average recorded score for each attendance
-- category, excluding rows where the score is NULL.
--
-- IMPORTANT:
-- Verify that CGPA and percentage values use a consistent
-- scale before interpreting their combined average.
-- ==========================================================

SELECT
    attendance_category,
    COUNT(*) AS total_students,
    ROUND(
        AVG(current_cgpa_or_percentage)::numeric,
        2
    ) AS average_recorded_score
FROM public.student_study_habits_clean
WHERE current_cgpa_or_percentage IS NOT NULL
GROUP BY attendance_category
ORDER BY average_recorded_score DESC;


-- ==========================================================
-- 9. STUDY HOURS VS. RECORDED ACADEMIC SCORE
-- Calculate the average recorded score for each study
-- category, excluding rows where the score is NULL.
--
-- This identifies associations, not proof of causation.
-- ==========================================================

SELECT
    study_category,
    COUNT(*) AS total_students,
    ROUND(
        AVG(current_cgpa_or_percentage)::numeric,
        2
    ) AS average_recorded_score
FROM public.student_study_habits_clean
WHERE current_cgpa_or_percentage IS NOT NULL
GROUP BY study_category
ORDER BY average_recorded_score DESC;