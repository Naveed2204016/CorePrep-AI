-- Run once against an existing database before enabling job-description roadmaps.
-- Existing single-subject topics remain valid with NULL and use roadmap.subject.
ALTER TABLE roadmap_topics ADD COLUMN curriculum_subject VARCHAR(100) NULL;
