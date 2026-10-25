-- Rules v2 (plan section 10a): interim closes (first / second close, raised to date) are recorded as
-- their own fund event so that a fund still raising is never shown as a final fund size.
alter table core.fund drop constraint fund_event_check;
alter table core.fund add constraint fund_event_check check (event in
    ('first_close', 'interim_close', 'final_close', 'launch', 'target', 'commitment', 'other'));
