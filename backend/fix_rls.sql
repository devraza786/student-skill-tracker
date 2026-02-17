-- Run this in the Supabase SQL Editor to disable RLS 
-- This allows your backend to perform CRUD operations without authentication.

-- Run this to clear all data and start IDs from 1
TRUNCATE students, skills, student_skills RESTART IDENTITY CASCADE;

ALTER TABLE students DISABLE ROW LEVEL SECURITY;
ALTER TABLE skills DISABLE ROW LEVEL SECURITY;
ALTER TABLE student_skills DISABLE ROW LEVEL SECURITY;

-- If you prefer to keep RLS ON and add a "Select All" policy instead, use this:
-- CREATE POLICY "Enable access to all users" ON "public"."students" AS PERMISSIVE FOR ALL TO public USING (true);
