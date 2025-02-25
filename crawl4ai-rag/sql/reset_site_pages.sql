-- Delete all rows from the table.
-- The Supabase UI will warn you that you are above to run a destructive query.
delete from site_pages where 1=1;

-- Verify that all rows have been deleted.
select count(*) from site_pages;
