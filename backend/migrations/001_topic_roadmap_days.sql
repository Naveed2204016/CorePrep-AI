-- Run once against the existing Railway MySQL database before deploying this release.
ALTER TABLE roadmap_topics ADD COLUMN start_day INT NULL;
ALTER TABLE roadmap_topics ADD COLUMN end_day INT NULL;

-- Preserve any rows created by the earlier prototype.
UPDATE roadmap_topics
SET start_day = COALESCE(start_day, (`order` * 7) + 1),
    end_day = COALESCE(end_day, ((`order` + GREATEST(duration_weeks, 1)) * 7));

ALTER TABLE roadmap_topics MODIFY start_day INT NOT NULL;
ALTER TABLE roadmap_topics MODIFY end_day INT NOT NULL;
